from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken
from common.models import Model
from fcm_django.models import FCMDevice

from phonenumber_field.modelfields import PhoneNumberField

from cart.models import Cart

class User(AbstractUser):
    phone = PhoneNumberField(unique=True)
    email = models.EmailField(blank=True, null= True, unique=True)

    # TODO: something about the default value
    otp = models.CharField(max_length=4, default=0000)

    # True after first otp validation
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.email.lower().strip()
        if self.email == "":
            self.email = None
        super(User, self).save(*args, **kwargs)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    def full_name(self):
        return self.first_name + " " + self.last_name
    
    def generate_otp(self):
        self.otp = 1234
        self.save()
    
    def send_otp(self):
        self.generate_otp()
        # providor = CommunicationProvider()
        # providor.send_otp(otp=self.otp, number=str(self.phone))
    
    def check_otp(self, otp):
        if self.otp == otp:
            if not self.is_verified:
                self.is_verified = True
                self.save()
            return True
        return False
    
    def get_auth_tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }
    
    def get_devices(self):
        devices = FCMDevice.objects.filter(user=self)
        return devices if devices else None
    
    def sub_to_topic(self, topic):
        instance = NotificationTopic.objects.filter(code=topic).first()
        if instance:
            instance.users.add(self)
            devices = self.get_devices()
            if devices:
                devices.handle_topic_subscription(True, topic=topic)
    
    def register_fcm(self, token):
        user = self

        # Delete every device related to that token
        devices = FCMDevice.objects.filter(registration_id=token)
        devices.delete()

        # Register the token to the user
        device = FCMDevice.objects.create(user=user, registration_id=token)    
        
        # Registering user to user's stored topics
        for topic in user.notification_topics.all():
            device.handle_topic_subscription(True, topic=topic.code)
    
    def deregister_fcm(self, token):
        user = self
        device = FCMDevice.objects.filter(registration_id=token).first()
        if device:
            # Deregistering user from user's stored topics
            for topic in user.notification_topics.all():
                device.handle_topic_subscription(False, topic=topic.code)
            device.delete()

    
    def is_consumer(self):
        return True if hasattr(self, 'consumer') else False
    def is_store_owner(self):
        return True if hasattr(self, 'storeowner') else False
    def is_partner(self):
        return True if hasattr(self, 'partner') else False
    def is_salesman(self):
        return True if hasattr(self, 'salesman') else False
    def is_support(self):
        return True if hasattr(self, 'support') else False
    def is_sub_admin(self):
        return True if hasattr(self, 'subadmin') else False

class Consumer(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return "Consumer: {}".format(self.user.full_name())

    def save(self, *args, **kwargs):
        super(Consumer, self).save(*args, **kwargs)
    
    def get_cart(self):
        if hasattr(self, 'cart'):
            return self.cart
        else:
            cart = Cart(consumer=self)
            cart.save()
            return cart

class StoreOwner(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "StoreOwner: {}".format(self.user.full_name())

    def save(self, *args, **kwargs):
        super(StoreOwner, self).save(*args, **kwargs)

class Partner(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Partner: {}".format(self.user.full_name())

    def save(self, *args, **kwargs):
        super(Partner, self).save(*args, **kwargs)

class Salesman(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Salesman: {} ".format(self.user.full_name())

    def save(self, *args, **kwargs):
        super(Salesman, self).save(*args, **kwargs)

class Support(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Support: {}".format(self.user.full_name())

    def save(self, *args, **kwargs):
        super(Support, self).save(*args, **kwargs)

class SubAdmin(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Sub Admin: {}".format(self.user.full_name())

    def save(self, *args, **kwargs):
        super(SubAdmin, self).save(*args, **kwargs)

class NotificationTopic(Model):
    code = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    description = models.CharField(max_length=100, null=True, blank=True)
    users = models.ManyToManyField(User, related_name='notification_topics', blank=True)
    
    def __str__(self):
        return self.name
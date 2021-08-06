from django.db import models
from django.contrib.auth.models import AbstractUser
from common.models import Model

from phonenumber_field.modelfields import PhoneNumberField

from cart.models import Cart

class User(AbstractUser):
    phone = PhoneNumberField(unique=True)

    # TODO: something about the default value
    otp = models.CharField(max_length=4, default=0000)

    # True after first otp validation
    is_verified = models.BooleanField(default=False)

    is_consumer = models.BooleanField(default=False)
    is_partner = models.BooleanField(default=False)
    is_salesman = models.BooleanField(default=False)
    is_support = models.BooleanField(default=False)
    is_sub_admin = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name + " " + self.last_name
    
    def generate_otp(self):
        # TODO: abra ka dabra, OTP bhejdo
        self.otp = 1234
        self.save()
    
    def check_otp(self, otp):
        if self.otp == otp:
            if not self.is_verified:
                self.is_verified = True
                self.save()
            return True
        return False

class Consumer(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    def __str__(self):
        return "Consumer: {} {}".format(self.user.first_name, self.user.last_name)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.is_consumer = True
            self.user.save()
        super(Consumer, self).save(*args, **kwargs)
    
    def get_cart(self):
        if hasattr(self, 'cart'):
            return self.cart
        else:
            cart = Cart(consumer=self)
            cart.save()
            return cart

class Partner(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Partner: {} {}".format(self.user.first_name, self.user.last_name)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.is_partner = True
            self.user.save()
        super(Partner, self).save(*args, **kwargs)

class Salesman(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Salesman: {} {}".format(self.user.first_name, self.user.last_name)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.is_salesman = True
            self.user.save()
        super(Salesman, self).save(*args, **kwargs)

class Support(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Support: {} {}".format(self.user.first_name, self.user.last_name)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.is_support = True
            self.user.save()
        super(Support, self).save(*args, **kwargs)

class SubAdmin(Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return "Sub Admin: {} {}".format(self.user.first_name, self.user.last_name)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.user.is_sub_admin = True
            self.user.save()
        super(SubAdmin, self).save(*args, **kwargs)
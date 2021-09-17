from common.mixins import ValidateSerializerMixin
from rest_framework import generics, response
from common.permissions import *

from accounts.models import *
from accounts.serializers.general import *
from django.forms.models import model_to_dict

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = ( permissions.IsAuthenticated, )
    queryset = User.objects.all()

    def get_object(self):
        user_modal = self.request.user
        return user_modal
        user = model_to_dict(user_modal)
        if user['is_consumer'] and user_modal.consumer:
            return { **user, **model_to_dict(user_modal.consumer) }
        if user['is_sub_admin'] and user_modal.subadmin:
            return { **user, **model_to_dict(user_modal.subadmin) }
        if user['is_partner'] and user_modal.partner:
            return { **user, **model_to_dict(user_modal.partner) }
        if user['is_support'] and user_modal.support:
            return { **user, **model_to_dict(user_modal.support) }   
        if user['is_salesman'] and user_modal.salesman:
            return { **user, **model_to_dict(user_modal.salesman) }         
        return user

class RegisterTopicsView(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = TopicsRegisterSerializer
    permission_classes = ( permissions.IsAuthenticated, )
    
    def post(self, request):
        data = self.validate(request)
        user = request.user
        invalid_topics = []
        for topic in data['topics']:
            try:
                instance = NotificationTopic.objects.get(code=topic)
                user.notification_topics.add(instance)
            except NotificationTopic.DoesNotExist:
                invalid_topics.append(topic)
        return response.Response({
            'success': True,
            'invalid_topics': invalid_topics 
        })

class TopicsList(generics.ListAPIView):
    serializer_class = TopicsSerializer
    permission_classes = ( permissions.IsAuthenticated, )
    queryset = NotificationTopic.objects.all()

    def get_queryset(self):
        user = self.request.user
        return user.notification_topics.all()

class AddToken(generics.GenericAPIView, ValidateSerializerMixin):
    serializer_class = AddTokenSerializer
    permission_classes = ( permissions.IsAuthenticated, )
    
    def post(self, request):
        data = self.validate(request)
        user = request.user
        user.fcm_tokens = user.fcm_tokens + [data['token']]
        user.save()
        return response.Response({
            'success': 'Tokens Added'
        })
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

# class AddToken(generics.GenericAPIView, ValidateSerializerMixin):
#     serializer_class = AddTokenSerializer
#     permission_classes = ( permissions.IsAuthenticated, )
    
#     def post(self, request):
#         data = self.validate(request)
#         user = request.user
        
#         return response.Response({
#             'success': 'Token Added'
#         })

# class RemoveToken(generics.GenericAPIView, ValidateSerializerMixin):
#     serializer_class = AddTokenSerializer
#     permission_classes = ( permissions.IsAuthenticated, )
    
#     def post(self, request):
#         data = self.validate(request)
#         user = request.user
#         temp = user.fcm_tokens
#         temp.remove(data['token'])
#         temp = list(set(temp))
#         print(temp)
#         user.fcm_tokens = temp
#         user.save()
#         return response.Response({
#             'success': 'Token Removed'
#         })
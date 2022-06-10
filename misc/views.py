from django.http.response import HttpResponse
from django.shortcuts import render

from rest_framework import parsers, permissions, serializers, views, exceptions, response, status, generics
from common.communication_provider import CommunicationProvider
from motorwash.storage_backends import MediaStorage

from misc.serializers import *
from store.models import Store
from common.models import Service
from common.permissions import IsStoreOwner, IsPartner, IsSalesman, IsSubAdmin

import os

class FeedbackView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = FeedbackSerializer
    throttle_scope = "public_post_api"

    def perform_create(self, serializer):
        user = self.request.user
        if not user.is_anonymous:
            serializer.save(user=user)
        else:
            serializer.save()

class ContactView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = ContactSerializer
    throttle_scope = "public_post_api"


class ImageUploadParser(parsers.FileUploadParser):
    media_type = 'image/*'

class StoreImageUpload(views.APIView):
    serializer_class = ImageSerializer
    permission_classes = ( (IsSalesman | permissions.IsAdminUser ) , )
    parser_class = (ImageUploadParser,)

    def put(self, request, format=None):
        if 'image' not in request.data:
            raise exceptions.ParseError("No image found")

        file_obj = request.FILES.get('image')

        file_directory_within_bucket = 'user_upload_files/{username}'.format(username=request.user)
        file_path_within_bucket = os.path.join(
            file_directory_within_bucket,
            file_obj.name
        )

        media_storage = MediaStorage()
        media_storage.save(file_path_within_bucket, file_obj)
        file_url = media_storage.url(file_path_within_bucket)

        return response.Response({
            "url": file_url,
        }, status=status.HTTP_201_CREATED)

class DangerView(views.APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        print('inside danger')
        while(True):
            pass
        return HttpResponse(status=status.HTTP_200_OK)

class HealthCheck(views.APIView):
    permission_classes = (permissions.AllowAny, )

    def get(self, request, format=None):
        return HttpResponse("I'm fine! How are you?", status=status.HTTP_200_OK)

class SendGridEventView(views.APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, format=None):
        data = request.data
        for event in data:
            SendGridEmailEvent.objects.create(
                email = event.get('email'),
                smtpId = event.get('smtp-id'),
                event = event.get('event'),
                category = event.get('category'),
                sgEventId = event.get('sg_event_id'),
                sgMessageId = event.get('sg_message_id'),
                response = event.get('response'),
                reason = event.get('reason'),
                status = event.get('status'),
                useragent = event.get('useragent'),
                ip = event.get('ip'),
                url = event.get('url'),
            )
        return HttpResponse(status=status.HTTP_200_OK)

class TransportEnquiryView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = TransportEnquirySerializer
    throttle_scope = "public_post_api"
    
    def perform_create(self, serializer):
        to_city = self.request.data.get('to_city')
        from_city = self.request.data.get('from_city')
        serializer.save()
        CommunicationProvider.send_email(
            email=['d365labs@gmail.com', 'vermasubodhk@gmail.com'],
            subject='New Transport Enquiry from {} to {}'.format(from_city, to_city),
            html_content='''
                <h4>New Transportation Enquiry</h4> \n\n
                From: <strong>{}</strong> \n\n
                To: <strong>{}</strong> \n\n
                See all enquiries at <a href="https://api.autoave.in/admin/misc/transportenquiry/">https://api.autoave.in/admin/misc/transportenquiry/</a> \n\n
            '''.format(from_city, to_city),
        )
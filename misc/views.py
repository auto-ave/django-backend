from django.http.response import HttpResponse
from django.shortcuts import render

from rest_framework import parsers, permissions, serializers, views, exceptions, response, status, generics
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
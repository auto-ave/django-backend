from django.shortcuts import render

from rest_framework import parsers, views, exceptions, response, status, generics
from misc.models import StoreImage, ServiceImage
from misc.serializers import StoreImageSerializer, ServiceImageSerializer
from store.models import Store
from common.models import Service

class ImageUploadParser(parsers.FileUploadParser):
    media_type = 'image/*'

class StoreImageUpload(views.APIView):
    serializer_class = StoreImageSerializer
    parser_class = (ImageUploadParser,)
    # TODO: permissions
    # permission_classes = 

    def put(self, request, format=None):
        if 'image' not in request.data:
            raise exceptions.ParseError("No image found")

        image = request.data['image']
        store = request.data['store']

        instance = StoreImage()
        instance.store = Store.objects.get(pk=store)
        instance.image.save(image.name, image, save=True)
        instance.save()

        return response.Response(
            data={
                "url": instance.image.url
            },
            status=status.HTTP_201_CREATED
        )

class ServiceImageUpload(views.APIView):
    serializer_class = ServiceImageSerializer
    parser_class = (ImageUploadParser,)
    # TODO: permissions
    # permission_classes = 

    def put(self, request, format=None):
        if 'image' not in request.data:
            raise exceptions.ParseError("No image found")

        image = request.data['image']
        service = request.data['service']

        instance = ServiceImage()
        instance.service = Service.objects.get(pk=service)
        instance.image.save(image.name, image, save=True)
        instance.save()

        return response.Response(
            data={
                "url": instance.image.url
            },
            status=status.HTTP_201_CREATED
        )
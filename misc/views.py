from django.http.response import HttpResponse
from django.shortcuts import render

from rest_framework import parsers, permissions, serializers, views, exceptions, response, status, generics

from misc.serializers import *
from store.models import Store
from common.models import Service
from common.permissions import IsStoreOwner, IsPartner, IsSalesman, IsSubAdmin

class FeedbackView(generics.CreateAPIView):
    permission_classes = (permissions.AllowAny, )
    serializer_class = FeedbackSerializer
    throttle_scope = "public_post_api"


class ImageUploadParser(parsers.FileUploadParser):
    media_type = 'image/*'

class StoreImageUpload(views.APIView):
    serializer_class = ImageSerializer
    # permission_classes = ((IsStoreOwner | IsSalesman | IsPartner | IsSubAdmin | permissions.IsAdminUser) ,)
    # parser_class = (ImageUploadParser,)
    # TODO: everything
    # permission_classes = 

    def put(self, request, format=None):

        # if 'image' not in request.data:
        #     raise exceptions.ParseError("No image found")

        # image = request.data['image']
        # store = request.data['store']

        # instance = StoreImage()
        # instance.store = Store.objects.get(pk=store)
        # instance.image.save(image.name, image, save=True)
        # instance.save()

        return response.Response(
            data={
                "url": "https://static.toiimg.com/thumb/msid-83539139,width-1200,height-900,resizemode-4/.jpg"
            },
            status=status.HTTP_201_CREATED
        )

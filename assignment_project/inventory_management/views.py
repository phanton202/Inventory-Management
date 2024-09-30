from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Item
from django.shortcuts import get_object_or_404
from .serializers import ItemSerializer, UserRegSerializer
from rest_framework import status
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from rest_framework.decorators import api_view
import logging
from django.http import Http404


logger = logging.getLogger("testlogger")


@api_view(["POST"])
def register(request):
    serializer = UserRegSerializer(data=request.data)
    if serializer.is_valid():
        if User.objects.filter(username=request.data["email"]).exists():
            return Response(
                {"message": "User already exists"}, status=status.HTTP_400_BAD_REQUEST
            )
        user = User.objects.create(
            username=request.data["email"],
            email=request.data["email"],
            password=make_password(request.data["password"]),
        )
        user.save()
        return Response(
            {"message": "User Registered Successfully"}, status=status.HTTP_201_CREATED
        )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ItemView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, pk=None):
        logger.info(f"{request.user} => {request.method} {request.path}")
        if pk:
            try:

                item = get_object_or_404(Item, pk=pk)
                serializer = ItemSerializer(item)
                logger.info(serializer.data)
                return Response(serializer.data)
            except Http404 as e:
                logger.error(f"{request.user} => Item ID {pk} not found")
                raise e
        else:
            items = Item.objects.all()
            serializer = ItemSerializer(items, many=True)
            return Response(serializer.data)

    def post(self, request):
        logger.info(f"{request.user} => {request.method} {request.path} data[{request.data}]")
        serializer = ItemSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.user} => {request.method} {request.path} Item Saved:{serializer.data}")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"{request.user} => {request.method} {request.path} {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            item = get_object_or_404(Item, pk=pk)
        except Http404 as e:
            logger.error(f"{request.user} => {request.method} {request.path} Item ID {pk} not found")
            raise e
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"{request.user} => {request.method} {request.path} Item Updated:{serializer.data}")
            return Response(serializer.data)
        logger.error(f"{request.user} => {request.method} {request.path} {serializer.errors}")
        return Response(serializer.errors)

    def delete(self, request, pk):
        try:
            item = get_object_or_404(Item, pk=pk)
        except Http404 as e:
            logger.error(f"{request.user} => {request.method} {request.path} Item ID {pk} not found")
            raise e
        item.delete()
        logger.info(f"{request.user} => {request.method} {request.path} Item deleted: {item.name}")
        return Response(status=status.HTTP_204_NO_CONTENT)

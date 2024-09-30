from rest_framework import serializers
from .models import Item
from django.contrib.auth.models import User


class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ["id", "name", "desc", "quantity", "price"]


class UserRegSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "password"]

        extra_kwargs = {
            "email": {"required": True, "allow_blank": False},
            "password": {"required": True, "allow_blank": False},
        }

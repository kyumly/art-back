from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from art.models import Post, PostFile, Comment
from util.firebase import firebase_storage
from util import myModel
from users.models import User


class publicUserSerializer(ModelSerializer):


    class Meta:
        model = User
        fields = (
            "uuid",
            "id",
            "phone_number",
            "name",
            "username",
            "user_type"
        )

class privateUserSerializer(ModelSerializer):
    password = serializers.CharField(
        max_length=255,
        read_only=True
    )

    class Meta:
        model = User
        fields = (
            "uuid",
            "id",
            "phone_number",
            "name",
            "username",
            "user_type",
            'password'
        )
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from art.models import Post, PostFile, Comment
from util.firebase import firebase_storage
from util import myModel
from users.Serializers import UserSerializer


class publicPostCommentSerializer(ModelSerializer):
    user = UserSerializer.publicUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'uuid',
            'content',
            'created_time',
            'user',
        ]



class privatePostCommentSerializer(ModelSerializer):
    user = UserSerializer.publicUserSerializer(read_only=True)

    class Meta:
        model = Comment
        fields = [
            'uuid',
            'content',
            'created_time',
            'user',
        ]
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from art.models import Post, PostFile, Comment
from util.firebase import firebase_storage
from util import myModel
from users.Serializers import UserSerializer


class publicPostCommentSerializer(ModelSerializer):
    user = UserSerializer.publicUserSerializer(read_only=True)

    posts_title = serializers.SerializerMethodField()

    def get_posts_title(request, comment : Comment):
        return comment.post.title

    class Meta:
        model = Comment
        fields = [
            'uuid',
            'content',
            'created_time',
            'user',
            'posts_title'
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
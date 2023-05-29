from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from art.models import Post, PostFile
from util.firebase import firebase_storage
from util import myModel


class publicPostFileSerializer(ModelSerializer):
    file_url = serializers.SerializerMethodField()

    def get_file_url(self, post):
        return firebase_storage.FirebaseCustom.getFirebase(post.file_url)

    class Meta:
        model = PostFile
        fields = [
            'uuid',
            "file_name",
            "file_url",
            "file_type",
        ]

class privatePostFileSerializer(ModelSerializer):
    class Meta:
        model = PostFile
        fields = "__all__"


class publicPostSerializer(ModelSerializer):

    postfile = publicPostFileSerializer(read_only=True)

    class Meta:
        model = Post
        fields = [
            "uuid",
            'created_time',
            'last_update_time',
            'title',
            'content',
            'address',
            'postfile'
        ]


class privatePostSerializer(ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = Post
        fields = [
            "uuid",
            'created_time',
            'last_update_time',
            'title',
            'content',
            'address',
            'file'
        ]

    def create(self, validation_data: dict):
        file = validation_data.pop("file")

        #나중에 수정하기
        post = Post.objects.create(
            **validation_data
        )

        firebase = firebase_storage.FirebaseCustom(
            file=file, uuid=post.uuid
        )
        path = firebase.uploadFirebase(user_uuid = post.user.uuid)

        file_model = myModel.Mymodel.setModel(PostFile, post_id=post.pk,
                                              file_type=file.content_type, file_url=path,
                                              file_name=file.name)
        file_model.save()

        return post


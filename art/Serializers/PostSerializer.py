from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from art.models import Post, PostFile
from util.firebase import firebase_storage
from util import myModel


class publicPostSeralizer(ModelSerializer):
    file = serializers.FileField(write_only=True)

    class Meta:
        model = Post
        fields = [
            "uuid",
            'file',
            'created_time',
            'last_update_time',
            'title',
            'content',
            'address',
            'file'
        ]

class privatePostSeralizer(ModelSerializer):
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
        path = firebase.uploadFirebase()

        file_model = myModel.Mymodel.setModel(PostFile, post_id=post.pk,
                                              file_type=file.content_type, file_url=path,
                                              file_name=file.name)
        file_model.save()

        return post
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
    file = serializers.FileField(read_only=True)

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

        file_model = self.upload(file, post)
        file_model.save()

        return post


    def update(self, instance : Post, validation_data:dict):
        for key, value in validation_data.items():
            if value == None:
                continue
            elif key == "file":
                validation_data.pop("file")
                print(value)

                delete =firebase_storage.FirebaseCustom.deleteFirebase(instance.uuid, instance.postfile.file_name)

                if delete:
                    instance.postfile.delete()
                    file_model = self.upload(value, instance)
                    file_model.save()
                else:
                    raise ("수정에 실패했습니다.")
                break
            else:
                setattr(instance, key, value)
        instance.save(update_fields=list(validation_data.keys()))
        return instance


    def upload(self, file, post):
        firebase = firebase_storage.FirebaseCustom(
            file=file, uuid=post.uuid
        )
        path = firebase.uploadFirebase(user_uuid=post.user.uuid)
        file_model = myModel.Mymodel.setModel(PostFile, post_id=post.pk,
                                              file_type=file.content_type, file_url=path,
                                              file_name=file.name)
        return file_model

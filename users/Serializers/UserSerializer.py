from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from art.models import Post, PostFile, Comment
from util.firebase import firebase_storage
from util import myModel
from users.models import User, DisabilityInfo
from rest_framework.exceptions import ParseError

class publicUserDisability(ModelSerializer):

    class Meta:
        model = DisabilityInfo
        fields = [
            'uuid',
            'register_number',
            'file_name',
            'file_type',
            'file_url',
        ]

class publicUserSerializer(ModelSerializer):

    disability = serializers.SerializerMethodField()

    def get_disability(self, user):
        disability = DisabilityInfo.objects.filter(user = user)
        if disability:
            return publicUserDisability(disability[0]).data
        else:
            return "정보가 없습니다."

    class Meta:
        model = User
        fields = (
            "uuid",
            "id",
            "phone_number",
            "name",
            "username",
            "user_type",
            "disability",
        )

class privateUserSerializer(ModelSerializer):
    password = serializers.CharField(
        max_length=255,
        write_only=True
    )
    file = serializers.FileField(
        read_only=True
    )
    register_number= serializers.CharField(
        max_length=2555,
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
            'password',
            'file',
            'register_number'
        )


    def create(self, validated_data):
        type = validated_data['user_type']
        if type == "장애":
            file = validated_data.pop("file")
            register_number = validated_data.pop('register_number')

            user = User.objects.create(
                **validated_data
            )
            file_model = self.upload(file, user, register_number)
            file_model.save()

        else:
            user = User.objects.create(
                **validated_data
            )
        user.set_password(validated_data['password'])
        user.save(update_fields=['password'])

        return user

    def update(self, instance : User, validation_data):

        file = validation_data.pop("file")
        register_number = validation_data.pop('register_number')

        user_type= instance.user_type

        if user_type == "장애":

            if register_number:
                instance.disability.register_number = register_number
                instance.save()


            if file:
                delete = firebase_storage.FirebaseCustom.deleteFirebase(instance.uuid, instance.disability.file_name)

                if delete == True:
                    n_register_number = instance.disability.register_number

                    instance.disability.delete()

                    file_model = self.upload(file, instance, n_register_number)
                    file_model.save()
                else:
                    raise ("수정에 실패했습니다.")


        for key, value in validation_data.items():
            setattr(instance, key, value)
        return instance

        # for key, value in validation_data.items():
        #     if value == None:
        #         continue
        #     elif key == "file":
        #         print(value)
        #
        #         delete = firebase_storage.FirebaseCustom.deleteFirebase(instance.uuid, instance.postfile.file_name)
        #
        #         if delete == True:
        #             instance.postfile.delete()
        #             file_model = self.upload(value, instance)
        #             file_model.save()
        #         else:
        #             raise ("수정에 실패했습니다.")
        #         break
        #     elif
        #     else:
        #         setattr(instance, key, value)
        # instance.save(update_fields=list(validation_data.keys()))
        # return instance



    def upload(self, file, user, register_number):
        firebase = firebase_storage.FirebaseCustom(
            file=file, uuid=user.uuid
        )
        path = firebase.uploadFirebase(user_uuid=user.uuid)
        file_model = myModel.Mymodel.setModel(DisabilityInfo, user_id=user.pk,
                                              file_type=file.content_type, file_url=path,
                                              file_name=file.name, register_number = register_number)
        return file_model
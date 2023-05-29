from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from art.models import Post
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
            'user',
            'file'
        ]
    def create(self, validation_data):
        print(validation_data)

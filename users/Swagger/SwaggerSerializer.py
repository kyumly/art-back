from rest_framework import serializers

class getRequestUserModifedSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)



class getRequestLoginSerializer(serializers.Serializer):
    login = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=255)


class getRequestCommentSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=255)

class getResponseSerializer(serializers.Serializer):
    status = serializers.CharField()
    message = serializers.CharField()

class getRequestPostSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=255
    )
    content = serializers.CharField(
        max_length=4000
    )
    address = serializers.CharField(
        max_length=255
    )
    file = serializers.FileField()
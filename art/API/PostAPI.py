from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from django.db import transaction
from art.Serializers import  PostSerializer
from art.models import Post

from users.models import User


class Posts(APIView):
    serializer_class = PostSerializer.privatePostSeralizer

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer.publicPostSeralizer(posts, many=True)
        return Response(
            serializer.data
        )


    def post(self, request):
        serializer = PostSerializer.privatePostSeralizer(data=request.data)
        if serializer.is_valid():

            post = serializer.save(user_id = 2)

            post.save()
            serializer = PostSerializer.publicPostSeralizer(
                post
            )
            return  Response(
                serializer.data
            )
        else:
            return Response(
                serializer.errors
            )




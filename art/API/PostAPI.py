from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import transaction
from art.Serializers import  PostSerializer
from art.models import Post
from util import myModel
from util.firebase import firebase_storage
from rest_framework.exceptions import ParseError
from users.models import User
from util.permission import  IsOwnerOrReadOnly

class Posts(APIView):
    serializer_class = PostSerializer.privatePostSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer.publicPostSerializer(posts, many=True)
        return Response(
            serializer.data
        )


    def post(self, request):
        serializer = PostSerializer.privatePostSerializer(data=request.data)
        file = request.data.get('file', None)
        if not file:
            raise ParseError("첨부파일이 없습니다.")
        if serializer.is_valid():

            post = serializer.save(file = file , user_id = 2)

            post.save()
            serializer = PostSerializer.publicPostSerializer(
                post
            )
            return  Response(
                serializer.data
            )
        else:
            return Response(
                serializer.errors
            )

class PostDetail(APIView):
    permission_classes = [IsOwnerOrReadOnly]

    serializer_class = PostSerializer.privatePostSerializer



    def get(self, request, id):
        post = myModel.Mymodel.getModel(Post, uuid = id)
        return Response(
            PostSerializer.publicPostSerializer(post).data
        )

    def put(self, request, id):
        post = myModel.Mymodel.getModel(Post, uuid = id)
        serializer =PostSerializer.privatePostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            file = request.data.get('file', None)
            if file:
                post = serializer.save(file=file)
            else:
                post = serializer.save()
            serializer = PostSerializer.publicPostSerializer(post)
            return Response(
                serializer.data
            )

        else :
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


    def delete(self, request, id):

        post = Post.objects.select_related('user').get(uuid= id)

        try:
            with transaction.atomic() :
                post_uuid = post.uuid
                delete = firebase_storage.FirebaseCustom.deleteFirebase(post_uuid, post.postfile.file_name)
                if delete:
                    post.delete()
                    return Response(
                        {"result" : 'ok'},
                        status=status.HTTP_204_NO_CONTENT,
                    )
                else:
                    post.delete()
                    raise ParseError("삭제에 실패했습니다.")
        except Exception as e:

            raise  status.HTTP_400_BAD_REQUEST("삭제에 실패함")
from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import transaction
from art.Serializers import  PostSerializer
from art.models import Post
from users.Swagger import SwaggerSerializer
from util import myModel
from util.firebase import firebase_storage
from rest_framework.exceptions import ParseError
from users.models import User
from util.permission import  IsOwnerOrReadOnly

class Posts(APIView):
    serializer_class = PostSerializer.privatePostSerializer

    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(tags=["전체 게시글"],
                         responses={"200": PostSerializer.publicPostSerializer})
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer.publicPostSerializer(posts, many=True)
        return Response(
            serializer.data
        )


    @swagger_auto_schema(tags=["전체 작성하기"],
                         request_body=SwaggerSerializer.getRequestPostSerializer,
                         responses={"200": PostSerializer.publicPostSerializer})
    def post(self, request):
        """
        notice
        "file" : 파일
        json (X) -> multipart
        """
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




    @swagger_auto_schema(tags=["게시글 자세히 보기"],
                         responses={"200": PostSerializer.publicPostSerializer})
    def get(self, request, id):
        post = myModel.Mymodel.getModel(Post, uuid = id)
        return Response(
            PostSerializer.publicPostSerializer(post).data
        )

    @swagger_auto_schema(tags=["게시글 자세히 수정"],
                         request_body=SwaggerSerializer.getRequestPostSerializer,
                         responses={"200": PostSerializer.publicPostSerializer})
    def put(self, request, id):
        """
        notice
        "file" : 파일
        json (X) -> multipart
        """
        post = myModel.Mymodel.getModel(Post, uuid = id)
        serializer =PostSerializer.privatePostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid():
            file = request.data.get('file', None)
            if file:
                post = serializer.save(file=file)
            else:
                post = serializer.save()

            pk = post.pk
            post = Post.objects.get(pk= pk)

            serializer = PostSerializer.publicPostSerializer(post)
            return Response(
                serializer.data
            )

        else :
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


    @swagger_auto_schema(tags=["게시글 삭제"])
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
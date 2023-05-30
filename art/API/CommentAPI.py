from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import transaction
from art.Serializers import  PostSerializer, CommentSerializer
from art.models import Post, Comment
from util import myModel
from util.firebase import firebase_storage
from rest_framework.exceptions import ParseError
from users.models import User

from util.permission import IsOwnerOrReadOnly

from rest_framework.permissions import IsAuthenticatedOrReadOnly


class PostDetailComment(APIView):
    permission_classes = [IsOwnerOrReadOnly ,IsAuthenticatedOrReadOnly]

    serializer_class = CommentSerializer.publicPostCommentSerializer



    def get(self, request, id):
        post = Comment.objects.select_related('post').filter(post__uuid=id)

        return Response(
            CommentSerializer.publicPostCommentSerializer(post, many=True).data
        )

    def post(self, request, id):
        user = request.user
        serializer = CommentSerializer.privatePostCommentSerializer(data=request.data)

        post = Post.objects.filter(uuid = id).values("pk")[0]
        if serializer.is_valid():
            comment = serializer.save(user= user, post_id = post['pk'])
            return Response(
                CommentSerializer.publicPostCommentSerializer(comment).data
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )


class PostDetailCommentDetail(APIView):

    serializer_class = CommentSerializer.privatePostCommentSerializer

    permission_classes = [IsOwnerOrReadOnly, IsAuthenticatedOrReadOnly]


    def get(self, request, id, comment_id):
        comment = myModel.Mymodel.getModel(Comment, uuid = comment_id)
        return Response(
            CommentSerializer.publicPostCommentSerializer(comment).data
        )

    def put(self, request, id, comment_id):
        comment = myModel.Mymodel.getModel(Comment, uuid = comment_id)
        serializer = CommentSerializer.privatePostCommentSerializer(comment, data= request.data, partial=True)
        if serializer.is_valid():
            comment = serializer.save()
            return Response(
                CommentSerializer.publicPostCommentSerializer(
                    comment
                ).data
            )
        else:
            return Response(
                serializer.errors
            )
    def delete(self, request, id, comment_id):
        comment = myModel.Mymodel.getModel(Comment, uuid = comment_id)
        try:
            comment.delete()
            return Response(
                {"result" : "ok"},
                status=status.HTTP_204_NO_CONTENT
            )
        except Exception as e:
            print(e)
            raise ParseError("comment 삭제 오류")




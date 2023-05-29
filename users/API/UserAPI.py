from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import transaction
from users.Serializers import UserSerializer
from art.models import Post, Comment
from util import myModel
from util.firebase import firebase_storage
from rest_framework.exceptions import ParseError
from users.models import User

class Me(APIView):
    serializer_class = UserSerializer.privateUserSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        serializer = UserSerializer.publicUserSerializer(user)
        return Response(
            serializer.data
        )
    def put(self, request):
        user = request.user
        serializer = UserSerializer.privateUserSerializer(user, partial=True, data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            password = request.data.get("password", None)
            if password:
                user.set_password(password)
                user.save(update_fields=['password'])


            return Response(
                UserSerializer.publicUserSerializer(user).data
            )
        else:
            return Response(
                serializer.errors
            )

    def delete(self, request):
        pass



class Register(APIView):
    serializer_class = UserSerializer.privateUserSerializer


    def get(self, request):
        user = request.user
        serializer = UserSerializer.publicUserSerializer(user)
        return Response(
            serializer.data
        )
class Refresh(APIView):
    serializer_class = UserSerializer.privateUserSerializer


    def get(self, request):
        user = request.user
        serializer = UserSerializer.publicUserSerializer(user)
        return Response(
            serializer.data
        )
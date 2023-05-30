from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from django.db import transaction
from users.Serializers import UserSerializer
from rest_framework.exceptions import ParseError
from users.models import User
from django.contrib.auth import authenticate, login, logout
from config.authentication import JWTAuthentication

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

            file = request.data.get("file", None)
            register_number = request.data.get("register_number", None)


            user = serializer.save(file = file, register_number = register_number)
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

    def post(self, request):
        serializer = UserSerializer.privateUserSerializer(data=request.data)

        if serializer.is_valid():
            if request.data.get('user_type', None) == "장애":
                file = request.data.get('file', None)
                register_number = request.data.get('register_number', None)
                if not file and not register_number:
                    raise ParseError("file or register_number 빠졌습니다.")
                user = serializer.save(file=file, register_number = register_number)
            else :
                user = serializer.save()

            return Response(
                UserSerializer.publicUserSerializer(user).data
            )
        else:
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

# class Refresh(APIView):
#     serializer_class = UserSerializer.privateUserSerializer
#
#
#     def get(self, request):
#         user = request.user
#         serializer = UserSerializer.publicUserSerializer(user)
#         return Response(
#             serializer.data
#         )

class LogIn(APIView):
    """
    {
    "id" : "skkim3360",
    "password" : "1234"
    }
    """
    def post(self, request):
        username = request.data.get("id")
        password = request.data.get("password")

        if not username or not password:
            raise ParseError
        user = authenticate(request, id=username, password =password)

        if user:
            payload = {
                "userId" : user.uuid.hex,
            }
            token = JWTAuthentication.generate_token(payload, type="access")
            return Response(
                {
                    'token' : token
                }
            )
        else:
            return Response(
                {"error" : "비밀번호 오류"}
            )



class Comments(APIView):
    def get(self, request):
        pass



class Posts(APIView):
    pass

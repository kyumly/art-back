from django.urls import path, include
from users.API import UserAPI
urlpatterns = [
    path('me', UserAPI.Me.as_view()),
    path('login', UserAPI.LogIn.as_view()),

    path('register', UserAPI.Register.as_view()),

    path('comments', UserAPI.Comments.as_view()),

    path('posts', UserAPI.Posts.as_view()),

]
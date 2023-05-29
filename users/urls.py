from django.urls import path, include
from users.API import UserAPI
urlpatterns = [
    path('me', UserAPI.Me.as_view()),
    path('login', UserAPI.LogIn.as_view())


]
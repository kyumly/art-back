from django.urls import path
from art.API import  PostAPI, ReportAPI, PostAPI

urlpatterns = [
    path('posts', PostAPI.Posts.as_view())
]
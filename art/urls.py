from django.urls import path
from art.API import  PostAPI, ReportAPI, PostAPI, CommentAPI

urlpatterns = [
    path('posts', PostAPI.Posts.as_view()),
    path('posts/<uuid:id>', PostAPI.PostDetail.as_view()),

    path('posts/<uuid:id>/comments', CommentAPI.PostDetailComment.as_view()),
    path('posts/<uuid:id>/comments/<uuid:comment_id>', CommentAPI.PostDetailCommentDetail.as_view())

]

from django.urls import path, include
from users.API import UserAPI
urlpatterns = [
    path('me', UserAPI.Me.as_view()),
    path('login', UserAPI.LogIn.as_view()),

    path('register', UserAPI.Register.as_view()),

    path('me/comments', UserAPI.Comments.as_view()),

    path('me/comments/<uuid:comment_id>', UserAPI.CommentsDetail.as_view()),

    path('me/posts', UserAPI.Posts.as_view()),

    path('me/posts/<uuid:post_id>', UserAPI.PostsDetail.as_view()),

]
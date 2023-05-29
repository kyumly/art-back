from django.db import models
from common.models import CommonModel

# Create your models here.
from users.models import User


class Post(CommonModel):
    """
    1. 작품 파일
    2. 제목
    3. 내용
    4. 전시주소
    5. 작성자
    6. 작성 시간
    7. 수정 일자
    """
    file = models.URLField(
        max_length=255,
    )

    title = models.CharField(
        max_length=255
    )

    content = models.TextField()

    address = models.TextField(null=True)

    user = models.ForeignKey(
        User,
        related_name="post",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "Post"


class Comment(CommonModel):
    """
    1. 내용
    2. 닉네임
    3. 작성시간
    """
    post = models.ForeignKey(
        Post,
        related_name="comment",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        User,
        related_name="comment",
        on_delete=models.CASCADE,
    )
    class Meta:
        db_table = "Comment"


class report(CommonModel):
    content = models.TextField()

    user = models.ForeignKey(
        User,
        related_name="report",
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = "Report"

class PostFile(CommonModel):
    post = models.ForeignKey(
        Post,
        related_name='postfile',
        on_delete=models.CASCADE
    )

    file_name = models.CharField(
        max_length=200
    )

    file_url = models.URLField(max_length=500)

    file_type = models.CharField(
        max_length=200
    )

    class Meta:
        db_table = "PostFile"


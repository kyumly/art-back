from django.db import models

# Create your models here.

import uuid

class CommonModel(models.Model):
    """
    Common Model Definition
    """

    seq = models.AutoField(primary_key=True)

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    created_time = models.DateTimeField(auto_now_add=True)

    last_update_time = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True


class UserType(models.TextChoices):
    """
    졸업, 재학중, 휴학중, 중퇴, 자퇴, 졸업예정
    """
    disability = ("장애")
    ability = ("일반")

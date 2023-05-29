from django.db import models

# Create your models here.

import uuid

class CommonModel(models.Model):
    """
    Common Model Definition
    """
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    created_time = models.DateTimeField(auto_now_add=True)

    last_update_time = models.DateTimeField(auto_now=True)


    class Meta:
        abstract = True

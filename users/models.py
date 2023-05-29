from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from common.models import CommonModel
import uuid

class UserManager(BaseUserManager):
    def create_user(self, id, password, **kwargs):
        """
        주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
        """
        if not id:
            raise ValueError('Users must have an email address')
        user = self.model(
            phone_number=id,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, id=None, password=None, **extra_fields):
        """
        주어진 이메일, 비밀번호 등 개인정보로 User 인스턴스 생성
        단, 최상위 사용자이므로 권한을 부여
        """
        print(extra_fields)
        superuser = self.create_user(id=id, password=password, **extra_fields)

        superuser.is_admin = True
        superuser.is_superuser = True
        superuser.is_active = True

        superuser.save(using=self._db)
        return superuser



# Create your models here.
class User(AbstractBaseUser, CommonModel):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)

    id = models.CharField(
        max_length=255,
        unique=True,
        null=False
    )
    name = models.CharField(
        max_length=255,
        null=False
    )

    username = models.CharField(
        unique=True,
        max_length=255,
        null=False
    )
    phone_number = models.CharField(
        unique=True,
        max_length=255,
        null=False
    )

    register_number = models.CharField(
        unique=True,
        max_length=255,
        null=False
    )


    objects = UserManager()

    USERNAME_FIELD = 'id'

    is_admin = models.BooleanField(default=False)

    REQUIRED_FIELDS = []

    class Meta:
        db_table = "Users"



    @property
    def is_staff(self):
        return self.is_admin


    def __str__(self):
        return f"{self.uuid} {self.name}"

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin

    @is_staff.setter
    def is_staff(self, value):
        self._is_staff = value



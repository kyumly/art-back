from rest_framework.exceptions import (
    NotFound, PermissionDenied, NotAuthenticated, ParseError
)
from django.db import transaction

class Mymodel:
    def __init__(self):
        pass

    @staticmethod
    def getModel(model, **kwargs):
        try:
            return model.objects.get(**kwargs)
        except model.DoesNotExist:
            raise NotFound

    @staticmethod
    def getOneSelectModel(model, foreign, value, **kwargs):
        try:
            return model.objects.select_related(foreign).filter(**kwargs).values(value)
        except model.DoesNotExist:
            raise NotFound

    @staticmethod
    def setModel(model, **kwargs):
        try:
            return model(**kwargs)
        except Exception as e:
            print(e)
            raise NotFound("모델 만드는데 실패했습니다.")

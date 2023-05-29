import jwt
from rest_framework.authentication import BaseAuthentication
from users.models import User
from rest_framework.exceptions import AuthenticationFailed
from django.conf import settings
import datetime
class JWTAuthentication(BaseAuthentication):

    def authenticate(self, request):

        token = request.headers.get("JWT")
        if not token:
            return None
        try:
            decode = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        except Exception as e:
            raise AuthenticationFailed("jwt 인증 에러")



        pk = decode.get('userId')
        if not pk:
            return None
        try:
            user = User.objects.get(uuid=pk)
            return (user,None)
        except User.DoesNotExist:
            raise AuthenticationFailed("토큰 에러")

    @staticmethod
    def generate_token(payload, type):
        if type == "access":
            # 2시간
            exp = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
        elif type == "refresh":
            # 2주
            exp = datetime.datetime.utcnow() + datetime.timedelta(weeks=2)
        else:
            raise Exception("Invalid tokenType")

        payload['exp'] = exp
        payload['iat'] = datetime.datetime.utcnow()

        encoded = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

        return encoded
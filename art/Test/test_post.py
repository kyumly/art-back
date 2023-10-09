from rest_framework.test import APITestCase

from art.models import Post
from util.test_data import   POST_DATA, USER_DATA_ability, USER_DATA_disability
from users.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from util.firebase import firebase_storage
# Create your tests here.


class PostTestCase(APITestCase):
    URL = "/api/v1/posts"

    def setUp(self) -> None:
        User.objects.create(
            **USER_DATA_ability
        )
        user = User.objects.create(
            **USER_DATA_disability
        )
        user.set_password("1234")
        user.save()



    def test_post(self):
        file_content = b'This is a test file.'
        file = SimpleUploadedFile('test_file.txt', file_content, content_type='text/plain')
        POST_DATA['file'] = file


        login_data = {
            'id' : "skkim3530",
            'password' : "1234"
        }
        response = self.client.post(
            data=login_data,
            path=f"/api/v1/users/login",
            format='json'
        )
        jwt = response.data['token']

        response = self.client.post(
            path=self.URL,
            data=POST_DATA,
            format='multipart',
            HTTP_jwt = jwt
        )
        print("data : ", response.data)

        self.assertEqual(response.status_code, 200)
        firebase_storage.FirebaseCustom.deleteFirebase(response.data['uuid'], 'test_file.txt')


class PostDetailTestCase(APITestCase):
    URL = "/api/v1/posts"
    post1 = None
    post2 = None

    def setUp(self) -> None:
        user=User.objects.create(
            **USER_DATA_ability
        )
        self.post1 = Post.objects.create(
            **POST_DATA
        )
        self.post1.user = user
        self.post1.save()

        user2 = User.objects.create(
            **USER_DATA_disability
        )

        self.post2 = Post.objects.create(
            **POST_DATA
        )
        self.post2.user = user2
        self.post2.save()

    def test_post_detail(self):
        print("첨부파일 테스트 진행중")
        res = self.client.get(path=f"{self.URL}/{self.post1.uuid}")
        self.assertEqual(
            res.status_code, 200, '에러코드가 200이 아닙니다.'
        )

        print('res : ', res.data)



from rest_framework.test import APITestCase

from art.models import Post
from util.test_data import  *
from users.models import User
from django.core.files.uploadedfile import SimpleUploadedFile
from util.firebase import firebase_storage
# Create your tests here.


class PostTestCase(APITestCase):
    URL = "/api/v1/users"
    URL_POST = "/api/v1/posts"


    def setUp(self) -> None:

        user = User.objects.create(
            **USER_DATA_ability_2
        )
        user.set_password('4')
        user.save()
        # User.objects.create(
        #     **USER_DATA_disability
        # )
        post = Post.objects.create(
            **POST_DATA
        )
        post.user = user



    def test_nomal(self):
        file_content = b'This is a test file.'
        file = SimpleUploadedFile('test_file.txt', file_content, content_type='text/plain')

        #회원 가입
        response = self.client.post(
            data = USER_DATA_ability,
            path=f"{self.URL}/register",
            format='json'

        )
        #회원 가입 데이터
        print("회원가입 데이터 : ", response.data)
        self.assertEqual(response.status_code, 200)

        login_data = {
            'id' : response.data['id'],
            'password' : 1234
        }
        response = self.client.post(
            data=login_data,
            path=f"{self.URL}/login",
            format='json'
        )

        #로그인 데이터
        print("로그엔 데이터 : ", response.data)
        self.assertEqual(response.status_code, 200)

        jwt = response.data['token']


        response = self.client.get(
            path=f"{self.URL}/me",
            format='json',
            HTTP_JWT = jwt

        )

        #나의 정보 데이터
        print("user me ", response.data)
        self.assertEqual(response.status_code, 200)


        response = self.client.get(
            path=f"{self.URL_POST}",
        )

        print("게시물 데이터 : ", response.data)
        self.assertEqual(response.status_code, 200)

        # 로그인 안했을시
        response = self.client.post(
            path=f"{self.URL_POST}",
            data = POST_DATA,
        )
        self.assertEqual(response.status_code, 403, '로그인 가능해야 가입 가능함')


        response = self.client.post(
            path=f"{self.URL_POST}",
            data = POST_DATA,
            HTTP_JWT=jwt

        )
        self.assertEqual(response.status_code, 400, '첨부파일 없는데 값 들어감')
        print("error : ", response.data)

        POST_DATA['file'] = file
        response = self.client.post(
            path=f"{self.URL_POST}",
            data = POST_DATA,
            HTTP_JWT=jwt

        )
        #게시판 post 데이터
        print("respone post : ", response.data)
        self.assertEqual(response.status_code, 200, "게시물 등록 완료")


        post_uuid = response.data['uuid']
        response = self.client.get(
            path=f"{self.URL_POST}/{post_uuid}",
            HTTP_JWT=jwt
        )

        #게시판 post 데이터
        print("respone detail post : ", response.data)
        self.assertEqual(response.status_code, 200, "게시물 조회 완료")

        response = self.client.put(
            path=f"{self.URL_POST}/{post_uuid}",
            data={
                'title': "수정",
                "content": "내용수정",
            },
            format='json',
            HTTP_JWT=jwt
        )
        #이름 수정
        print("respone detail put : ", response.data)
        self.assertEqual(response.status_code, 200, "게시물 조회 완료")

        #첨부파일 수정
        file_content = b'This is a test file2.'
        file = SimpleUploadedFile('test_file2.txt', file_content, content_type='text/plain')

        response = self.client.put(
            path=f"{self.URL_POST}/{post_uuid}",
            data={
                'title': "수정2",
                "content": "내용수정2",
                'file' : file
            },
            format='multipart',
            HTTP_JWT=jwt
        )

        # 이름 수정 & 첨부파일 수정
        print("respone detail put 첨부파일 : ", response.data)
        self.assertEqual(response.status_code, 200, "게시물 조회 완료")

        #코멘트 달기
        response = self.client.post(
            path=f"{self.URL_POST}/{post_uuid}/comments",
            data=COMMENT_DATA,
            format='json',
        )
        print("코멘트 실패 : ", response.data)
        self.assertEqual(response.status_code, 403, "회원 가입 후 댓글 가능")

        #코멘트 달기
        response = self.client.post(
            path=f"{self.URL_POST}/{post_uuid}/comments",
            data=COMMENT_DATA,
            HTTP_JWT=jwt,
            format='json',
        )

        print("코멘트 값 넣기 : ", response.data)
        self.assertEqual(response.status_code, 200, "댓글 기입 성공")

        #댓글 가져오기
        response = self.client.get(
            path=f"{self.URL_POST}/{post_uuid}/comments",
        )
        print("코멘트 값 가져오기 : ", response.data)
        self.assertEqual(response.status_code, 200, "댓글 기입 성공")

        comment_id = response.data[0]['uuid']

        response = self.client.get(
            path=f"{self.URL_POST}/{post_uuid}/comments/{comment_id}",
        )

        print("코멘트 값 가져오기 : ", response.data)
        self.assertEqual(response.status_code, 200, "작성한 댓글 가쟈오기")


        #댓글 수정하기
        response = self.client.put(
            path=f"{self.URL_POST}/{post_uuid}/comments/{comment_id}",
            data={
                "content" : "수정진행중입니다."
            },
            # HTTP_JWT=jwt,
            format='json',
        )

        print("코멘트 수정진행중 가져오기 : ", response.data)
        self.assertEqual(response.status_code, 403, "작성한 댓글 가쟈오기")


        login_data = {
            'id' : '1',
            'password' : '4'
        }
        response = self.client.post(
            data=login_data,
            path=f"{self.URL}/login",
            format='json'
        )
        print(response.data)
        jwt2 = response.data['token']

        #댓글 수정하기 - 값 넣기
        response = self.client.put(
            path=f"{self.URL_POST}/{post_uuid}/comments/{comment_id}",
            data={
                "content" : "수정진행중입니다."
            },
            HTTP_JWT=jwt2,
            format='json',
        )

        print("코멘트 수정진행중 가져오기 : ", response.data)
        self.assertEqual(response.status_code, 200, "작성한 댓글 가쟈오기")














# class PostDetailTestCase(APITestCase):
#     URL = "/api/v1/posts"
#     post1 = None
#     post2 = None
#
#     def setUp(self) -> None:
#         user=User.objects.create(
#             **USER_DATA_ability
#         )
#         self.post1 = Post.objects.create(
#             **POST_DATA
#         )
#         self.post1.user = user
#         self.post1.save()
#
#         user2 = User.objects.create(
#             **USER_DATA_disability
#         )
#
#         self.post2 = Post.objects.create(
#             **POST_DATA
#         )
#         self.post2.user = user2
#         self.post2.save()
#
#     def test_post_detail(self):
#         print("첨부파일 테스트 진행중")
#         res = self.client.get(path=f"{self.URL}/{self.post1.uuid}")
#         self.assertEqual(
#             res.status_code, 200, '에러코드가 200이 아닙니다.'
#         )
#
#         print('res : ', res.data)



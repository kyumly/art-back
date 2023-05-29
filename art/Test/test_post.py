from django.test import TestCase
from util.test_data import   POST_DATA, USER_DATA_ability, USER_DATA_disability
from users.models import User
# Create your tests here.


class PostTestCase(TestCase):
    URL = "/api/v1/posts"

    def setUp(self) -> None:
        User.objects.create(
            **USER_DATA_ability
        )
        User.objects.create(
            **USER_DATA_disability
        )


    def test_post(self):
        self.client.post(
            path=self.URL,
            data=POST_DATA,
            format='json'
        )
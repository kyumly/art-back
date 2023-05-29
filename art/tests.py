from django.test import TestCase

# Create your tests here.


class PostTestCase(TestCase):
    URL = "/api/v1/posts"

    def test_post(self):
        self.client.post(
            path=self.URL
        )
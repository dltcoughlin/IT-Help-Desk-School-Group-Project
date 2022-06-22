from django.test import Client, TestCase

class TestHome(TestCase):
    def setup(self) -> None:
        self.client = Client()

    '''renders home page'''
    def test_home_page(self) -> None:
        response = self.client.get('/app/')
        self.assertEqual(response.content, b"Hello, authenticated user. You're at the home page")

from django.test import Client, TestCase

class TestIndex(TestCase):
    def setup(self) -> None:
        self.client = Client()

    '''renders index page'''
    def test_index_page(self) -> None:
        response = self.client.get('')
        self.assertEqual(response.content, b"Hello, world. You're at the IT Help landing page")

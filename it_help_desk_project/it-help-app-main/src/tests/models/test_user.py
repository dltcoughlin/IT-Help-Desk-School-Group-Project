from django.test import TestCase
from ..__init__ import User

class UserTest(TestCase):
    def setUp(self) -> None:
        User.objects.create(first_name="Ada", last_name="Lovelace", password="f3m413Pr0gr4mm3r")

    '''tests full name as a combo of first and last name'''
    def test_full_name(self) -> None:
        existing_user = User.objects.get(first_name="Ada")
        self.assertEqual(existing_user.full_name, 'Ada Lovelace')

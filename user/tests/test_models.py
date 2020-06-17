from django.test import TestCase
from django.contrib.auth import get_user_model
from unittest.mock import patch


class ModelTestCase(TestCase):
    def setUp(self):
        self.email = "test@example.com"
        self.password = "test-password"

    def tearDown(self):
        self.email = None
        self.password = None

    @staticmethod
    def _create_user(**kwargs):
        """ Create a sample user """
        return get_user_model().objects.create_user(**kwargs)

    def test_create_user_with_email_success(self):
        """ Testing to make sure creating a new user with email is successful """
        user = get_user_model().objects.create_user(
            email=self.email, password=self.password
        )
        self.assertEquals(user.email, self.email)
        self.assertTrue(user.check_password(self.password))

        # Delete user
        user.delete()

    def test_create_user_with_email_normalized(self):
        """ Testing to make sure emails for new user is normalized """
        email = "test@EXAMPLE.com"
        password = "test-password"
        user = get_user_model().objects.create_user(email=email, password=password)
        self.assertEquals(user.email, email.lower())

        # Delete user
        user.delete()

    def test_create_user_with_invalid_email(self):
        """ Testing to make sure we can't create users with invalid email """

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None, "test123")

    def test_create_user_as_superuser(self):
        """ Testing to make sure super users can be created """
        user = get_user_model().objects.create_superuser(self.email, self.password)

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

        # Delete user
        user.delete()

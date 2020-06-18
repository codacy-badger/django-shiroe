from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


class PublicUserAPITestCase(TestCase):
    def setUp(self):
        self.create_user_endpoint = reverse("user:create")
        self.token_endpoint = reverse("user:token")
        self.user_endpoint = reverse("user:manage")
        self.client = APIClient()

    def _create_user(self, **kwargs):
        user = get_user_model().objects.create_user(**kwargs)
        return user

    def test_create_valid_user_success(self):
        """ Test for creating user with valid payload """
        payload = {
            "email": "test@example.com",
            "password": "testpass",
            "name": "Test name",
        }
        response = self.client.post(self.create_user_endpoint, payload)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(**response.data)

        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", response.data)

    def test_user_already_exists(self):
        """ Test to check tthat user creation fails when a user already exists """
        payload = {"email": "test@example.com", "password": "testpass"}
        self._create_user(**payload)
        response = self.client.post(self.create_user_endpoint, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short(self):
        """ Test that the password is more than 8 characters """
        payload = {"email": "test@example.com", "password": "123"}
        response = self.client.post(self.create_user_endpoint, payload)

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_token_creation(self):
        """ Test that token is created for the user """
        payload = {"email": "test@example.com", "password": "password123"}
        self._create_user(**payload)
        response = self.client.post(self.token_endpoint, payload)

        self.assertIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_token_creation_with_invalid_credentials(self):
        """ Test token creation with invalid credentials """
        self._create_user(email="test@example.com", password="testpass")
        payload = {"email": "test@example.com", "password": "1234"}
        response = self.client.post(self.token_endpoint, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_token_creation_no_user(self):
        payload = {"email": "test@example.com", "password": "1234"}
        response = self.client.post(self.token_endpoint, payload)

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_token_missing_field(self):
        """ Test to make sure email and password is required """
        response = self.client.post(
            self.token_endpoint, {"email": "one", "password": ""}
        )

        self.assertNotIn("token", response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """ Test that authentication is required for users """
        response = self.client.get(self.user_endpoint)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTestCase(TestCase):
    """ Test api requests that require authentication """

    def setUp(self):
        self.user_endpoint = reverse("user:manage")
        self.user = self._create_user(
            email="test@example.com", password="testpass", name="John Doe"
        )
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def tearDown(self):
        self.user.delete()

    def _create_user(self, **kwargs):
        user = get_user_model().objects.create_user(**kwargs)
        return user

    def test_get_user_success(self):
        """ Test getting profile as logged in user """
        response = self.client.get(self.user_endpoint)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data, {"name": self.user.name, "email": self.user.email}
        )

    def test_post_not_allowed(self):
        """ Test that POST requests are not allowed on user endpoint"""
        response = self.client.post(self.user_endpoint, {})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        payload = {"name": "Test name", "password": "newpassword456"}
        response = self.client.patch(self.user_endpoint, payload)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, payload["name"])
        self.assertTrue(self.user.check_password(payload["password"]))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

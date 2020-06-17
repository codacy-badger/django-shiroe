from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse


class AdminTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            email="admin@gmail.com", password="password456", name="TTest Bame"
        )
        self.client.force_login(self.admin_user)
        self.user = get_user_model().objects.create_user(
            email="user@example.com", password="password123", name="Test User"
        )

    def tearDown(self):
        self.client = None
        self.admin_user.delete()
        self.user.delete()

    def test_get_users(self):
        """ Test to make sure all users are listed """
        url = reverse("admin:user_user_changelist")
        response = self.client.get(url)

        self.assertContains(response, self.user.name)
        self.assertContains(response, self.user.email)

    def test_user_edit_page(self):
        """ Test to make sure the user edit page works """
        url = reverse("admin:user_user_change", args=[self.user.id])
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

    def test_user_create_page(self):
        """ Test to make sure create user page works """
        url = reverse("admin:user_user_add")
        response = self.client.get(url)

        self.assertEquals(response.status_code, 200)

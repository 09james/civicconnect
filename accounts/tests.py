"""Tests for account registration and role enforcement."""

from django.test import TestCase, override_settings
from django.urls import reverse

from .models import User


class CitizenRegistrationTests(TestCase):
    """Ensure public signup always creates a citizen."""

    def test_registration_creates_citizen_and_logs_in(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newcitizen",
                "first_name": "New",
                "last_name": "Citizen",
                "email": "citizen@example.com",
                "password1": "StrongPass!123",
                "password2": "StrongPass!123",
            },
        )
        user = User.objects.get(username="newcitizen")
        self.assertEqual(user.role, User.Role.CITIZEN)
        self.assertFalse(user.is_staff)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(int(self.client.session["_auth_user_id"]), user.pk)

    def test_registration_rejects_password_mismatch(self):
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "anothercitizen",
                "email": "another@example.com",
                "password1": "StrongPass!123",
                "password2": "DifferentPass!123",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="anothercitizen").exists())

    def test_admin_login_redirects_to_dashboard(self):
        User.objects.create_user(
            username="operator",
            password="StrongPass!123",
            role=User.Role.ADMIN,
        )
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "operator", "password": "StrongPass!123"},
        )
        self.assertRedirects(response, reverse("requests:admin_dashboard"))


@override_settings(ADMIN_BOOTSTRAP_TOKEN="test-only-bootstrap-token")
class InitialAdminSetupTests(TestCase):
    """Verify initial administrator provisioning is private and one-time."""

    def setUp(self):
        self.url = reverse("accounts:initial_admin_setup")
        self.form_data = {
            "username": "firstadmin",
            "email": "admin@example.com",
            "password1": "VeryStrongPass!9382",
            "password2": "VeryStrongPass!9382",
            "bootstrap_token": "test-only-bootstrap-token",
        }

    def test_first_superuser_can_be_created_once(self):
        response = self.client.post(self.url, self.form_data)
        user = User.objects.get(username="firstadmin")
        self.assertRedirects(response, reverse("accounts:login"))
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)
        self.assertEqual(user.role, User.Role.ADMIN)
        self.assertEqual(self.client.get(self.url).status_code, 404)

    def test_invalid_setup_token_does_not_create_user(self):
        self.form_data["bootstrap_token"] = "incorrect-token"
        response = self.client.post(self.url, self.form_data)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(User.objects.filter(username="firstadmin").exists())

    def test_setup_page_is_disabled_without_configured_token(self):
        with override_settings(ADMIN_BOOTSTRAP_TOKEN=""):
            response = self.client.get(self.url)
        self.assertEqual(response.status_code, 404)

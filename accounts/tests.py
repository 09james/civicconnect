"""Tests for account registration and role enforcement."""

from django.test import TestCase
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

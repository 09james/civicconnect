"""Tests for request privacy, status updates, and administrator access."""

from django.test import TestCase
from django.urls import reverse

from accounts.models import User
from .models import Category, ServiceRequest


class ServiceRequestTests(TestCase):
    """Verify access control and request status timestamp behavior."""

    def setUp(self):
        self.citizen = User.objects.create_user(
            username="citizen", password="StrongPass!123"
        )
        self.other_citizen = User.objects.create_user(
            username="other", password="StrongPass!123"
        )
        self.admin = User.objects.create_user(
            username="operator",
            password="StrongPass!123",
            role=User.Role.ADMIN,
        )
        self.category = Category.objects.create(name="Water supply")
        self.service_request = ServiceRequest.objects.create(
            citizen=self.citizen,
            category=self.category,
            location="Main Street",
            description="A water pipe is leaking.",
        )

    def test_citizens_only_see_their_own_requests(self):
        self.client.force_login(self.other_citizen)
        response = self.client.get(reverse("requests:my_requests"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "A water pipe is leaking.")

    def test_citizen_cannot_access_admin_dashboard(self):
        self.client.force_login(self.citizen)
        response = self.client.get(reverse("requests:admin_dashboard"))
        self.assertEqual(response.status_code, 403)

    def test_admin_can_update_status_and_resolved_timestamp(self):
        self.client.force_login(self.admin)
        response = self.client.post(
            reverse("requests:update_status", args=[self.service_request.pk]),
            {"status": ServiceRequest.Status.RESOLVED},
        )
        self.assertRedirects(response, reverse("requests:admin_dashboard"))
        self.service_request.refresh_from_db()
        self.assertEqual(self.service_request.status, ServiceRequest.Status.RESOLVED)
        self.assertIsNotNone(self.service_request.resolved_at)

    def test_returning_to_open_state_clears_resolved_timestamp(self):
        self.service_request.status = ServiceRequest.Status.RESOLVED
        self.service_request.save()
        self.service_request.status = ServiceRequest.Status.IN_PROGRESS
        self.service_request.save()
        self.assertIsNone(self.service_request.resolved_at)

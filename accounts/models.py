"""User model and role definitions."""

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """A portal user with citizen or administrator permissions."""

    class Role(models.TextChoices):
        CITIZEN = "citizen", "Citizen"
        ADMIN = "admin", "Admin"

    role = models.CharField(
        max_length=10, choices=Role.choices, default=Role.CITIZEN
    )

    def save(self, *args, **kwargs):
        """Keep Django superusers in the administrator role."""
        if self.is_superuser:
            self.role = self.Role.ADMIN
        super().save(*args, **kwargs)

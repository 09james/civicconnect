"""Role-based access mixins for request views."""

from django.contrib.auth.mixins import AccessMixin
from django.core.exceptions import PermissionDenied

from accounts.models import User


class AdminRoleRequiredMixin(AccessMixin):
    """Require an authenticated user whose portal role is admin."""

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.role != User.Role.ADMIN:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)

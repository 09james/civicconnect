"""Authentication views for citizens."""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.db import connection, transaction
from django.http import Http404
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View
from django.views.decorators.http import require_http_methods

from .forms import CitizenRegistrationForm, InitialAdminSetupForm
from .models import User


class PortalLoginView(LoginView):
    """Send signed-in users to the dashboard for their role."""

    template_name = "accounts/login.html"

    def get_success_url(self):
        redirect_to = self.get_redirect_url()
        if redirect_to:
            return redirect_to
        if self.request.user.role == User.Role.ADMIN:
            return reverse("requests:admin_dashboard")
        return reverse("requests:my_requests")


class RegisterView(View):
    """Create a citizen account and sign the citizen in."""

    template_name = "accounts/register.html"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("requests:my_requests")
        return render(request, self.template_name, {"form": CitizenRegistrationForm()})

    def post(self, request):
        if request.user.is_authenticated:
            return redirect("requests:my_requests")
        form = CitizenRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Your citizen account has been created.")
            return redirect("requests:my_requests")
        return render(request, self.template_name, {"form": form})


@require_http_methods(["GET", "POST"])
def initial_admin_setup(request):
    """Create the first superuser through a temporary, token-protected page."""
    expected_token = settings.ADMIN_BOOTSTRAP_TOKEN
    if not expected_token or User.objects.filter(is_superuser=True).exists():
        raise Http404

    form = InitialAdminSetupForm(
        request.POST or None,
        expected_token=expected_token,
    )
    if request.method == "POST" and form.is_valid():
        with transaction.atomic():
            if connection.vendor == "postgresql":
                table_name = connection.ops.quote_name(User._meta.db_table)
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"LOCK TABLE {table_name} IN EXCLUSIVE MODE"
                    )
            if User.objects.filter(is_superuser=True).exists():
                raise Http404
            user = form.save()
        messages.success(
            request,
            "The initial administrator was created. You can now log in.",
        )
        return redirect("accounts:login")
    return render(request, "accounts/initial_admin_setup.html", {"form": form})

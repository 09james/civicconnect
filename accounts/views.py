"""Authentication views for citizens."""

from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render
from django.urls import reverse
from django.views import View

from .forms import CitizenRegistrationForm
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

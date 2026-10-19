"""Account URL routes."""

from django.contrib.auth import views as auth_views
from django.urls import path

from .views import PortalLoginView, RegisterView, initial_admin_setup

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", PortalLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path(
        "initial-admin-setup/",
        initial_admin_setup,
        name="initial_admin_setup",
    ),
]

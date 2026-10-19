"""Account URL routes."""

from django.contrib.auth import views as auth_views
from django.urls import path

from .views import PortalLoginView, RegisterView

app_name = "accounts"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", PortalLoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
]

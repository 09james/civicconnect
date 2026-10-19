"""Service request URL routes."""

from django.urls import path

from . import views

app_name = "requests"

urlpatterns = [
    path("", views.home, name="home"),
    path("my-requests/", views.MyRequestsView.as_view(), name="my_requests"),
    path("requests/new/", views.CreateRequestView.as_view(), name="create_request"),
    path("dashboard/", views.AdminDashboardView.as_view(), name="admin_dashboard"),
    path(
        "dashboard/requests/<int:pk>/status/",
        views.UpdateRequestStatusView.as_view(),
        name="update_status",
    ),
]

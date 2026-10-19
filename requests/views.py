"""Citizen and administrator service request views."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from accounts.models import User
from .forms import AdminRequestUpdateForm, ServiceRequestForm
from .models import Category, ServiceRequest
from .permissions import AdminRoleRequiredMixin


def home(request):
    """Render the public landing page."""
    return render(request, "requests/home.html")


class MyRequestsView(LoginRequiredMixin, View):
    """List only requests belonging to the current citizen."""

    template_name = "requests/my_requests.html"

    def get(self, request):
        service_requests = ServiceRequest.objects.filter(citizen=request.user).select_related(
            "category"
        )
        return render(
            request, self.template_name, {"service_requests": service_requests}
        )


class CreateRequestView(LoginRequiredMixin, View):
    """Create a service request for the signed-in citizen."""

    template_name = "requests/request_form.html"

    def get(self, request):
        return render(request, self.template_name, {"form": ServiceRequestForm()})

    def post(self, request):
        form = ServiceRequestForm(request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            service_request.citizen = request.user
            service_request.save()
            messages.success(request, "Your service request has been submitted.")
            return redirect("requests:my_requests")
        return render(request, self.template_name, {"form": form})


class AdminDashboardView(AdminRoleRequiredMixin, View):
    """Show all requests, filters, and basic service analytics."""

    template_name = "requests/admin_dashboard.html"

    def get(self, request):
        service_requests = ServiceRequest.objects.select_related(
            "citizen", "category"
        )
        status = request.GET.get("status", "")
        category = request.GET.get("category", "")
        query = request.GET.get("q", "").strip()
        if status in ServiceRequest.Status.values:
            service_requests = service_requests.filter(status=status)
        if category.isdigit():
            service_requests = service_requests.filter(category_id=int(category))
        if query:
            service_requests = service_requests.filter(
                Q(location__icontains=query)
                | Q(description__icontains=query)
                | Q(citizen__username__icontains=query)
            )

        categories = Category.objects.annotate(
            request_count=Count("service_requests")
        )
        context = {
            "service_requests": service_requests,
            "categories": categories,
            "category_choices": Category.objects.all(),
            "selected_status": status,
            "selected_category": category,
            "search_query": query,
            "open_count": ServiceRequest.objects.exclude(
                status=ServiceRequest.Status.RESOLVED
            ).count(),
            "resolved_count": ServiceRequest.objects.filter(
                status=ServiceRequest.Status.RESOLVED
            ).count(),
        }
        return render(request, self.template_name, context)


class UpdateRequestStatusView(AdminRoleRequiredMixin, View):
    """Update the status of a request from the administrator dashboard."""

    def post(self, request, pk):
        service_request = get_object_or_404(ServiceRequest, pk=pk)
        form = AdminRequestUpdateForm(request.POST, instance=service_request)
        if form.is_valid():
            form.save()
            messages.success(request, f"Request #{service_request.pk} status updated.")
        else:
            messages.error(request, "Choose a valid request status.")
        return redirect("requests:admin_dashboard")

"""Forms for citizen-submitted service requests."""

from django import forms

from .models import ServiceRequest


class ServiceRequestForm(forms.ModelForm):
    """Validate the request details submitted by a citizen."""

    class Meta:
        model = ServiceRequest
        fields = ("category", "location", "description", "image")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
        }
        help_texts = {
            "image": "Optional. Upload a JPG, PNG, or WebP image.",
        }

    def clean_image(self):
        image = self.cleaned_data.get("image")
        if image and image.size > 5 * 1024 * 1024:
            raise forms.ValidationError("Image files must be 5 MB or smaller.")
        return image


class AdminRequestUpdateForm(forms.ModelForm):
    """Allow administrators to update request status."""

    class Meta:
        model = ServiceRequest
        fields = ("status",)

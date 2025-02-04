from django import forms
from .models import Listings

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ["title", "price", "description"]

    description = forms.CharField(
    widget=forms.Textarea(
        attrs={"rows": 3, "class": "form-control", "style": "resize: none;"}
    )
)
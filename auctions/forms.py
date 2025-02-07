from django import forms
from .models import Listings, Comments

class ListingForm(forms.ModelForm):
    class Meta:
        model = Listings
        fields = ["title", "price", "description"]

    description = forms.CharField(
    widget=forms.Textarea(
        attrs={"rows": 3, "class": "form-control", "style": "resize: none;"}
    )
)
    
class CommentsForm(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['content']  
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Escreva seu comentário...'}),
        }
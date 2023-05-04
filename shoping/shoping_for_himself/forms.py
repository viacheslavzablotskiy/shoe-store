from .models import Track, User
from django.forms import ModelForm, TextInput


class TrackForm(ModelForm):
    class Meta:
        model = Track
        fields = ["name", ]

        widgets = {
            "name": TextInput(attrs={
                "class": "form-control",
                "placeholder": "name",
            }),

        }

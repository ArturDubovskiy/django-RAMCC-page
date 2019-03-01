from django import forms
from captcha.fields import CaptchaField
from .models import JoinClub

class JoinForm(forms.ModelForm):
    captcha = CaptchaField(label="", required=True)

    class Meta:
        model = JoinClub
        fields = ["first_name", "last_name", "date_of_birth", "email", "bio", "captcha"]
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Told us about yourself...'})
        }


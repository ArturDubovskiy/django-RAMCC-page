from django import forms
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User


class UserLoginForm(forms.Form):
    username = forms.CharField(label="Username")
    password = forms.CharField(widget=forms.PasswordInput, label="Password")

    def clean(self, *args, **kwargs):
        username = self.cleaned_data.get("username")
        password = self.cleaned_data.get("password")
        if username and password:
            user = authenticate(username=username, password=password)
            user_qs = User.objects.filter(username=username)
            if user_qs.count() == 1:
                user = user_qs.first()

            if not user:
                raise forms.ValidationError("This user does not exists")

            if not user.check_password(password):
                raise forms.ValidationError("Incorrect password")

            if not user.is_active:
                raise forms.ValidationError("User is not longer active")
        return super(UserLoginForm, self).clean(*args, *kwargs)


class UserRegisterForm(forms.ModelForm):
    email = forms.EmailField()
    email_2 = forms.EmailField(label="Confirm email")
    password = forms.CharField(widget=forms.PasswordInput)
    password_2 = forms.CharField(widget=forms.PasswordInput, label="Confirm password")

    class Meta:
        model = User
        fields = ['username',
                  'password',
                  'password_2',
                  'first_name',
                  'last_name',
                  'email',
                  'email_2'
                  ]

    def clean(self, *args, **kwargs):
        password = self.cleaned_data.get('password')
        password_2 = self.cleaned_data.get('password_2')

        if password != password_2:
            raise forms.ValidationError("Passwords not match")
        email = self.cleaned_data.get('email')
        email_2 = self.cleaned_data.get('email_2')
        if email != email_2:
            raise forms.ValidationError("Emails not match")
        email_qs = User.objects.filter(email=email)
        if email_qs.exists():
            raise forms.ValidationError("This email are already used")

        return super(UserRegisterForm, self).clean(*args, **kwargs)
from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from .forms import UserLoginForm, UserRegisterForm
from django.contrib import messages


class LoginView(View):
    title = "Login"

    def get(self, request):
        if request.user.is_authenticated:
            return redirect("news:post_list")
        form = UserLoginForm()
        return render(request, "user_auth/login_form.html", {"form": form, "title": self.title})

    def post(self, request):
        form = UserLoginForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect("news:post_list")
        return render(request, "user_auth/login_form.html", {"form": form, "title": self.title})


class RegisterView(View):
    title = "Register"

    def get(self, request):
        form = UserRegisterForm()
        print(form)
        return render(request, "user_auth/register_form.html", {"form": form, "title": self.title})


    def post(self, request):
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            user = form.save(commit=False)
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            login(request, user)
            messages.success(request, "Account created")
            return redirect("news:post_list")
        return render(request, "user_auth/register_form.html", {"form": form, "title": self.title})





class LogoutView(View):

    def get(self, request):
        logout(request)
        return redirect('login')
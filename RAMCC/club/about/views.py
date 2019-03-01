from django.contrib import messages
from django.shortcuts import render,  redirect
from django.views.generic import View
from .forms import JoinForm


class AboutView(View):

    def get(self, request):
        form = JoinForm()
        return render(request, 'about/about.html', {"name": "Artur", "form": form})

    def post(self, request):
        form = JoinForm(request.POST or None)
        if form.is_valid():
            join_form = form.save()
            join_form.save()
            messages.success(request, "Successfully sended")
        return redirect("about:about_us")

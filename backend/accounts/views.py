from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from .forms import ProfileForm, RegisterForm


def register(request):
    if request.user.is_authenticated:
        return redirect("post_login")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        #messages.success(request, "Compte créé, bienvenue sur HomeConnect !")
        return redirect("post_login")
    return render(request, "accounts/register.html", {"form": form})


@login_required
def profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Profil mis à jour.")
        return redirect("profile")
    return render(request, "accounts/profile.html", {"form": form})

@login_required
def post_login(request):
    if request.user.role == "client":
        return redirect("client_dashboard")
    return redirect("service_list")
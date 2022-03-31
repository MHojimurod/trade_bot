from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

from admin_panel.models import Operators


def login_required_decorator(f):
    return login_required(f, login_url="login")


def dashboard_login(request):
    if request.POST:
        username = request.POST.get("username")
        password = request.POST.get("password")
        try:
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("admin_panel:dashboard")
            else:
                return render(request, "login/login.html", {"error": "Invalid credentials"})
        except:
            usertye = Operators.objects.filter(username=username)
            if usertye:
                if usertye.first().active:
                    login(request, user)
                    return redirect("dashboard")
            else:
                if user is not None:
                    login(request, user)
                    return redirect("dashboard")
    return render(request, "dashboard/login.html")


@login_required_decorator
def dashboard_logout(request):
    logout(request)
    res = redirect("login")
    res.delete_cookie("sessionid")
    return res
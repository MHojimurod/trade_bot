from django.contrib.auth.decorators import login_required
from django.shortcuts import render,redirect
from django.contrib.auth import authenticate, login, logout

from admin_panel.models import Operators


def login_required_decorator(f):
    return login_required(f, login_url="login")


def dashboard_login(request):
    if request.POST:
        username = request.POST.get("username")
        operator = Operators.objects.filter(user__username__contains=username)
        password = request.POST.get("password")
        user = authenticate(username=username, password=password)
        if operator:
            if user is not None and operator.first().active:
                login(request, user)
                return redirect("home")
        else:
            if user is not None:
                login(request, user)
                return redirect("home")
    return render(request, "login/login.html")


@login_required_decorator
def dashboard_logout(request):
    logout(request)
    res = redirect("login")
    res.delete_cookie("sessionid")
    return res



def check_admin(request):
    if request.user:
        user = request.user
        if user is not None and  not user.is_anonymous:
            data = Operators.objects.filter(user=user)
            if data:
                access = data.first().pers
                ctx = {
                    "access_types":access
                }
                return ctx
        return {}
    return {}

from admin_panel.login.decorator import dashboard_login, login_required_decorator

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from admin_panel.models import Fillials, Operators
# Create your views here.


@login_required_decorator
def home(request):
    return render(request, 'dashboard/statistics/statistic.html')






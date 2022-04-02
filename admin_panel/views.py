
from admin_panel.login.decorator import dashboard_login, login_required_decorator

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout

from admin_panel.models import Fillials, Operators
# Create your views here.


@login_required_decorator
def home(request):
    return render(request, 'dashboard/settings/bot_settings.html')







def account(request):
    if request.method == 'POST':
        data = request.POST
        image = request.FILES
        print(image,"aaa")
        name = data["firstName"]
        surname = data["lastName"]
        username = data["username"]
        phone = data["phoneNumber"]
        country = data["country"]
        address = data["address"]
        Operators.objects.all().update(name=name, surname=surname, username=username, phone=phone, region=country, address=address)
        
    data = Operators.objects.all().first()
    return render(request, 'dashboard/operators/account.html', {'user_account': data})



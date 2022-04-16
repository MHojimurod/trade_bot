
from ast import operator
from calendar import c
from pyexpat import model
import re
from admin_panel.forms import OperatorForm
from admin_panel.login.decorator import dashboard_login, login_required_decorator
from django.contrib import  messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from admin_panel.models import Fillials, Operators
# Create your views here.


@login_required_decorator
def home(request):
    ctx = {"home":"active"}
    return render(request, 'dashboard/orders/list.html',ctx)



def account(request):
    if request.method == 'POST':
        data = request.POST
        image = request.FILES
        print(data,"aaa")
        name = data["firstName"]
        surname = data["lastName"]
        username = data["username"]
        phone = data["phoneNumber"]
        country = data["country"]
        address = data["address"]
        Operators.objects.all().update(name=name, surname=surname, username=username, phone=phone, region=country, address=address)
        messages.success(request, "Ma'lumotlar muvoffaqiyatli o'zgartirildi!")
        return redirect("account")
    data = Operators.objects.all().first()
    print(data)
    return render(request, 'dashboard/operators/account.html', {'user_account': data})



def list_operators(request):
    operators = Operators.objects.all()
    ctx = {"operators": operators,"operator_active":"active"}
    return render(request, 'dashboard/operators/list.html', ctx)

def create_operator(request):
    model = Operators()
    form = OperatorForm(request.POST,instance=model)
    if request.method == 'POST':
        if form.is_valid():
            if request.POST['password'] == request.POST['confirm_password']:
                form.save()
                return redirect("list_operator")
    ctx = {"form": form,"operator_active":"active"}
    return render(request,"dashboard/operators/create.html",ctx)

def edit_operator(request,pk):
    model = Operators.objects.get(pk=pk)
    form = OperatorForm(request.POST or None,instance=model)
    if request.POST:
        if form.is_valid():
            form.save()
            return redirect("list_operator")
    ctx = {"form": form,"operator_active":"active"}
    return render(request,"dashboard/operators/edit.html", ctx)

def delete_operator(request,pk):
    model = Operators.objects.get(pk=pk)
    model.delete()
    return redirect("list_operator") 
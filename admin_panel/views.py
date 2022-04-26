
from ast import operator
from calendar import c
from pyexpat import model
import re
from typing import Text
from django.http import HttpResponse

from requests import request
from admin_panel.forms import OperatorForm
from admin_panel.login.decorator import dashboard_login, login_required_decorator
from django.contrib import  messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from admin_panel.models import Fillials, Operators,Text
from django.contrib.auth.models import User as Djangouser
# Create your views here.   



@login_required_decorator
def home(request):
    data = {
    "order":"Buyurtma berish",
    "my_orders":"Mening buyurtmalarim",
    "busket":"Savatcha",
    "offers":"Telefon orqali aloqa",
    "our_addresses":"Bizning manzillar",
    "communications":"Aksiyalar",
    "settings":"Sozlamalar",
    "questions_and_adds":"Savol va takliflar",
    "add_more":"Yana qo'shish",
    "clearance":"Rasmiylashtirish",
    "send_location":"Lakatsiyangizni yuboring",
    "send_your_self_image":"Rasmingizni yuboring",
    "send_your_password_iamge":"Pasportingizni rasmini yuboring",
    "send_your_self_and_passport_image":"Pasportingizni ushlab turgan rasmini yiboring",
    "is_your_number":"{number} Shu raqamingiz to'g'rimi?",
    "yout_order_accepted":"Sizning buyurtmangiz qabul qilinde tez orada javobini aytamiz",
    "mainMenu":"Quyidagilarni birini tanlang",
    "send_name_and_surname":"Ism Familyangizni kiritng",
    "send_number_register":"Telefon raqamingizni yuboring",
    "send_number_register_button":"Yuborish",
    "select_filial":"Filliallardan birini tanlang",
    "successfully_registered":"Ro'yhatdan muvoffaqiyatli o'tdingiz",
    "support":"Savol yoki shikoyatingizni yo;llashingiz mumkin",
    "support_accepted":"Savol yoki shikoyatingiz qabul qilindi tez orada sizga javobini aytamiz",
    "contact_with_phone":"Biz bilan bog'lanish +998999999999",
    "settings_info":"Ismi: {_name}\nTelefon:{numher}\nTil:{lang}",
    "change_name":"Ismni o'zgartirish",
    "change_number":"Raqamni o'zgartirish",
    "change_language":"Tilni o'zgartirish"

}

    # for i,j in data.items():
    #     Text.objects.create(name=i,data=j,language_id=1)
    ctx = {"home":"active"}
    return render(request, 'dashboard/index.html',ctx)

def account(request):
    if request.POST or request.FILES:
        data = request.POST
        image = request.FILES.get("photo")
        name = data["firstName"]
        surname = data["lastName"]
        phone = data["phoneNumber"]
        country = data["country"]
        address = data["address"]
        operator = Operators.objects.get(user=request.user)
        operator.name=name
        operator.surname=surname
        operator.phone=phone
        operator.region=country
        operator.address=address
        if image:
            operator.photo = image
            operator.save()
        operator.save()
        messages.success(request, "Ma'lumotlar muvoffaqiyatli o'zgartirildi!")
        return redirect("account")
    data = Operators.objects.get(user=request.user)
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
            data = request.POST
            if request.POST['password'] == request.POST['confirm_password']:
                print(data["username"])
                if Djangouser.objects.filter(username=data['username']).exists():
                    messages.error(request, "Operator allaqachon bor")
                    return redirect("create_operator")
                else:
                    user = Djangouser.objects.create_user(
                        username=data["username"], password=data["password"], first_name=data["name"], last_name=data["surname"])
                    user.save()
                    print(user)
                    Operators.objects.create(
                        user=user,
                        phone=data["phone"],
                        pers=request.POST.getlist("pers"),
                        active=True if data.get("active") else False,
                    )
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
    user = Djangouser.objects.get(username=model.username)
    model.delete()
    user.delete()
    return redirect("list_operator") 



def error_message(request):
    messages.error(request,"Kechirasiz sizga bu bo'limga kirishga ruxsat yo'q")
    return redirect("home")
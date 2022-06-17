

from datetime import datetime
from admin_panel.forms import OperatorEditForm, OperatorForm
from admin_panel.login.decorator import dashboard_login, login_required_decorator
from django.contrib import  messages
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from admin_panel.models import Fillials, Operators,Text, User
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

    today_user = User.objects.filter(
        created_at__day=datetime.now().day).count()
    all_user = User.objects.all().count()
    uz_user = User.objects.filter(language__code="uz").count()
    ru_user = User.objects.filter(language__code="ru").count()
    ctx = {"home":"active",
        "today_user":today_user, #
        "all_user":all_user, #
        "total_percent":(100* today_user // all_user) if all_user else 0,
        "uz_percent":(100* uz_user // all_user) if all_user else 0,
        "ru_percent":(100* ru_user // all_user) if all_user else 0,
        "uz_user":uz_user, #
        "ru_user":ru_user}
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
    form = OperatorForm(request.POST,request.FILES,instance=model)
    if request.method == 'POST':
        if form.is_valid():
            data = request.POST
            image = request.FILES.get("photo")
            if request.POST['password'] == request.POST['confirm_password']:
                print(data["username"])
                if Djangouser.objects.filter(username=data['username']).exists():
                    messages.error(request, "Operator allaqachon bor")
                    return redirect("create_operator")
                else:
                    user = Djangouser.objects.create_user(
                        username=data["username"], password=data["password"], first_name=data["name"], last_name=data["surname"])
                    user.save()
                    Operators.objects.create(
                        user=user,
                        phone=data["phone"],
                        pers=request.POST.getlist("pers"),
                        active=True if data.get("active") else False,
                        photo=image
                    )
                return redirect("list_operator")
    ctx = {"form": form,"operator_active":"active"}
    return render(request,"dashboard/operators/create.html",ctx)

def edit_operator(request,pk):
    model = Operators.objects.get(pk=pk)
    form = OperatorEditForm(request.POST or None, request.FILES or None,instance=model)
    if request.POST:
        if form.is_valid():

            user_data = request.POST
            image = request.FILES.get("photo")
            print(image,"AAAAAAAAA")
            Djangouser.objects.filter(pk=model.user.id).update(first_name=user_data.get("name"),last_name=user_data.get("surname"))
            model.phone = user_data.get("phone")
            model.active = True if user_data.get("active") else False
            model.pers = request.POST.getlist("pers")
            if image is not None:
                model.photo = image
            model.save()
            messages.success(request,"Operator muvoffaqiyatli taxrirlandi")
            return redirect("list_operator")
    ctx = {"form": form,"operator_active":"active","data":model}
    return render(request,"dashboard/operators/edit.html", ctx)

def delete_operator(request,pk):
    model = Operators.objects.get(pk=pk)
    user = Djangouser.objects.get(id=model.user.id)
    model.delete()
    user.delete()
    messages.warning(request,"Operator muvoffaqiyatli o'chirildi")
    return redirect("list_operator") 



def error_message(request):
    messages.error(request,"Kechirasiz sizga bu bo'limga kirishga ruxsat yo'q")
    return redirect("home")
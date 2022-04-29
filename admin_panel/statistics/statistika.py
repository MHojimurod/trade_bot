from django.shortcuts import render
from admin_panel.models import BusketItem, Category, Fillials, User,Operators,Busket
from datetime import datetime
from django.db.models import Q

def all_statistika(request):
    today_user = User.objects.filter(
        created_at__day=datetime.now().day).count()
    all_user = User.objects.all().count()
    uz_user = User.objects.filter(language__code="uz").count()
    ru_user = User.objects.filter(language__code="ru").count()
    total_percent = 100* today_user // all_user
    uz_percent = 100* uz_user // all_user
    ru_percent = 100* ru_user // all_user
    
    categories = Category.objects.filter(parent=None)
    category_data = []
    for i in categories:
        for j in Category.objects.filter(parent=i):
            if len(category_data):
                for l in category_data:
                    if i.name_uz == l["category"]:
                        l.update({"data":l["data"]+BusketItem.objects.filter(product__category=j).count()})
                    else:
                        category_data.append({
                            "category":i.name_uz,
                            "data":BusketItem.objects.filter(product__category=j).count()
                        })
            else:
                category_data.append({
                    "category":i.name_uz,
                    "data":BusketItem.objects.filter(product__category=j).count()
                })



    operators = Operators.objects.all()
    fillials = Fillials.objects.all()
    fillial_data = []
    for j in fillials:
        fillial_data.append({
            "fillial":j.name_uz,
            "data":Busket.objects.filter(status=3,user__filial_id=j.id).count()
        })

    DATA = []
    for i in operators:
        DATA.append({   
            "operator":i.user.first_name,
            "accept":Busket.objects.filter(actioner=i,status=3).count(),
            "not_accept":Busket.objects.filter(actioner=i,status=4).count(),
            "archive":Busket.objects.filter(actioner=i,status=5).count(),
        })
    
    print(DATA)
    ctx = {
        "statistics_active": "active",
        "today_user":today_user, #
        "all_user":all_user, #
        "total_percent":total_percent,
        "uz_percent":uz_percent,
        "ru_percent":ru_percent,
        "uz_user":uz_user, #
        "ru_user":ru_user, #,
        "operators":DATA,
        "fillial_data":fillial_data,
        "category_data":category_data,
    }
    return render(request, 'dashboard/statistics/statistic.html',ctx)
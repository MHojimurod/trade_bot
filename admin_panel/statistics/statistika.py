from django.shortcuts import render
from admin_panel.models import BusketItem, Category, Fillials, User,Operators,Busket
from datetime import datetime

def all_statistika(request):
    today_user = User.objects.filter(
        created_at__day=datetime.now().day).count()
    all_user = User.objects.all().count()
    uz_user = User.objects.filter(language__code="uz").count()
    ru_user = User.objects.filter(language__code="ru").count()
    total_percent = 100* today_user // all_user
    uz_percent = 100* uz_user // all_user
    ru_percent = 100* ru_user // all_user
    
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
        "fillial_data":fillial_data
    }
    return render(request, 'dashboard/statistics/statistic.html',ctx)
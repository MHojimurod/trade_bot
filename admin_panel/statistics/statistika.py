from django.shortcuts import render
from admin_panel.models import BusketItem, Category, User,Operators,Busket
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
    DATA = []
    for i in operators:
        DATA.append({   
            "operator":i,
            "accept":Busket.objects.filter(actioner=1,status=3).count(),
            "not_accept":Busket.objects.filter(actioner=1,status=4).count(),

        })
    print(DATA)

    ctx = {
        "statistics_active": "active",
        "today_user":today_user,
        "all_user":all_user,
        "total_percent":total_percent,
        "uz_percent":uz_percent,
        "ru_percent":ru_percent,
        "uz_user":uz_user,
        "ru_user":ru_user
    }
    return render(request, 'dashboard/statistics/statistic.html',ctx)
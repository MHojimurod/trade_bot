from django.shortcuts import render


def all_statistika(request):
    ctx = {
        "statistics_active": "active",
    }
    return render(request, 'dashboard/statistics/statistic.html',ctx)
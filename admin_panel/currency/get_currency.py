import requests
from django.shortcuts import redirect
from admin_panel.models import BotSettings


def get_current_context(request):
    try:
        data  = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/")
        return {"currency":data.json()[0]}
    except:
        return {"currency":0}


def update_currency(request):
    if request.GET:
        if request.GET.get("currency"):
            if request.GET.get("currency").isdigit():
                BotSettings.objects.all().update(money=request.GET.get("currency"))
                # return redirect(str(request.path))
            else:
                return {}
        else:
            return {}
    return {"money":BotSettings.objects.first().money}


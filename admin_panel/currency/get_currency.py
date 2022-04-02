import requests

from admin_panel.models import BotSettings


def get_current_context(request):
    data  = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/")
    return {"currency":data.json()[0]}



def update_currency(request):
    if request.GET:
        if request.GET.get("currency"):
            if request.GET.get("currency").isdigit():
                BotSettings.objects.all().update(money=request.GET.get("currency"))
            else:
                return {}
        else:
            return {}
    return {"money":BotSettings.objects.first().money}


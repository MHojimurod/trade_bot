import requests
from django.shortcuts import redirect
from admin_panel.models import BotSettings, Operators


def get_current_context(request):
    try:
        data = 0
        # data  = requests.get("https://cbu.uz/uz/arkhiv-kursov-valyut/json/")
        # return {"currency":data.json()[0]}
        return {"currency":0}
    except:
        return {"currency":0}
    # return {"currency":0}


def update_currency(request):
    if request.GET:
        if request.GET.get("currency"):
            if request.GET.get("currency").isdigit():
                BotSettings.objects.all().update(money=request.GET.get("currency"))
                print("aaaa")
                # return redirect(str(request.path))
            else:
                return {}
        else:
            return {}
    x = BotSettings.objects.first()
    return {"money": x.money if x else 0}

def user_data(request):
    if not request.user.is_anonymous:
        if not request.user.is_superuser:
            operator = Operators.objects.get(user=request.user)
            return {
                "nav_operator":operator.user.first_name,
                "user_photo":operator.photo.url if operator.photo else "./static/dashboard/assets/img/default.png"
            }
        else:
            return  {
                "nav_operator":request.user.username,
                "user_photo":"/static/dashboard/assets/img/default.png"
            }
    return {}
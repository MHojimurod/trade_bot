
from django.shortcuts import render,redirect

from admin_panel.models import Color,Percent



def texts(request):
    return render(request, "dashboard/settings/text.html")

def settings(request):
    if request.POST:
        data = request.POST
        if data.get("yellow"):
            color = Color.objects.filter(color="sariq").update(base_percent=data.get("yellow"))
            
        if data.get("green"):
            color = Color.objects.filter(color="yashil").update(base_percent=data.get("green"))
        if data.get("red"):
            color = Color.objects.filter(color="qizil").update(base_percent=data.get("red"))
    YELLOW = Color.objects.filter(color="sariq").first()
    GREEN = Color.objects.filter(color="yashil").first()
    RED = Color.objects.filter(color="qizil").first()

    ctx = {
        "yellow":{"color":YELLOW,
                "3":Percent.objects.filter(color_id=YELLOW.id,months=3).first(),
                "6":Percent.objects.filter(color_id=YELLOW.id,months=6).first(),
                "12":Percent.objects.filter(color_id=YELLOW.id,months=12).first(),
                "24":Percent.objects.filter(color_id=YELLOW.id,months=24).first(),
                },
        "green":{"color":GREEN,
                "3":Percent.objects.filter(color_id=GREEN.id,months=3).first(),
                "6":Percent.objects.filter(color_id=GREEN.id,months=6).first(),
                "12":Percent.objects.filter(color_id=GREEN.id,months=12).first(),
                "24":Percent.objects.filter(color_id=GREEN.id,months=24).first(),
                },
        "red":{"color":RED,
                "3":Percent.objects.filter(color_id=RED.id,months=3).first(),
                "6":Percent.objects.filter(color_id=RED.id,months=6).first(),
                "12":Percent.objects.filter(color_id=RED.id,months=12).first(),
                "24":Percent.objects.filter(color_id=RED.id,months=24).first(),
                }
    }
    return render(request, "dashboard/settings/bot_settings.html",ctx)
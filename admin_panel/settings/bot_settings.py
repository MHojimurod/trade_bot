
import json
from django.shortcuts import render,redirect
from django.http import HttpResponse

from admin_panel.models import Color,Percent,Text,Language



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




def texts(request):
    

    languages: list[Language] = Language.objects.all()




    return render(request,"dashboard/settings/text.html",{
        "languages":languages
    })


def text_update(request):
    if request.body:
        body = json.loads(request.body.decode('utf-8'))

        for name, lang_val in body.items():
            for lang, val in lang_val.items():
                Text.objects.filter(name=name,language_id=lang).update(data=val)
    
        return HttpResponse("xxx")

def colors_update(request):
    color = request.POST.get("color")
    percent = request.POST.get(color)
    c = Color.objects.get(color=color)

    if c:
        three, six, twelve, twentyfour = request.POST.getlist("months")
        c.base_percent = percent
        c.save()
    
        percents = {
            "3":three,
            "6":six,
            "12":twelve,
            "24":twentyfour

        }
        for month, percent in percents.items():
            p = Percent.objects.filter(color_id=c.id,months=month)
            if p:
                p.percent = percent
                p.save()
            else:
                p = Percent(color_id=c.id,months=month,percent=percent)
                p.save()
    
    
    
    return redirect("settings")
    

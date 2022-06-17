
import json
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
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
    YELLOW = Color.objects.filter(color="Sariq").first()
    GREEN = Color.objects.filter(color="Yashil").first()
    RED = Color.objects.filter(color="Qizil").first()

    ctx = {
        "settings_active":"active","bot_active":"active","menu1_open":"open",
        "yellow":{"color":YELLOW,
                "3":Percent.objects.filter(color_id=YELLOW.id,months=3).first() if YELLOW else None ,
                "6":Percent.objects.filter(color_id=YELLOW.id,months=6).first() if YELLOW else None ,
                "12":Percent.objects.filter(color_id=YELLOW.id,months=12).first() if YELLOW else None ,
                "24":Percent.objects.filter(color_id=YELLOW.id,months=24).first() if YELLOW else None ,
                },
        "green":{"color":GREEN,
                "3":Percent.objects.filter(color_id=GREEN.id,months=3).first() if GREEN else None ,
                "6":Percent.objects.filter(color_id=GREEN.id,months=6).first() if GREEN else None ,
                "12":Percent.objects.filter(color_id=GREEN.id,months=12).first() if GREEN else None ,
                "24":Percent.objects.filter(color_id=GREEN.id,months=24).first() if GREEN else None ,
                },
        "red":{"color":RED,
                "3":Percent.objects.filter(color_id=RED.id,months=3).first() if RED else None ,
                "6":Percent.objects.filter(color_id=RED.id,months=6).first() if RED else None ,
                "12":Percent.objects.filter(color_id=RED.id,months=12).first() if RED else None ,
                "24":Percent.objects.filter(color_id=RED.id,months=24).first() if RED else None ,
                }
    }
    return render(request, "dashboard/settings/bot_settings.html",ctx)




def texts(request):
    languages: list[Language] = Language.objects.all()
    return render(request,"dashboard/settings/text.html",{
        "languages":languages,"settings_active":"active","text_active":"active","menu1_open":"open"
    })


def text_update(request):
    if request.body:
        body = json.loads(request.body.decode('utf-8'))

        for name, lang_val in body.items():
            for lang, val in lang_val.items():
                Text.objects.filter(name=name,language_id=lang).update(data=val)
        messages.success(request,"Ma'lumot saqlandi")
        return HttpResponse("xxx")

def colors_update(request):
    if request.POST:
        color = request.POST.get("color")
        percent = request.POST.get(color)
        print(color,"color")
        print(percent,"persent")
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
                p = Percent.objects.filter(color_id=c.id,months=month).first()
                if p:
                    p.percent = percent if percent else 0
                    p.save()
                else:
                    p = Percent(color_id=c.id,months=month,percent=percent)
                    p.save()
        messages.success(request,"Ma'lumot muvoffaqiyatli o'zgartirildi")
        
        
        
    return redirect("settings")
    

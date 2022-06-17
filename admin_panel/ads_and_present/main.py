from django.shortcuts import render, redirect
import requests
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db.models.fields.files import FieldFile
from admin_panel.forms import AdsForm
from admin_panel.models import Ads
from django.contrib import messages
def all_ads(request):
    ads = Ads.objects.order_by("-id").all()
    ctx = {
        "ads":ads,
        "ads_active":"active"
    }
    return render(request,"dashboard/ads_and_present/ads.html",ctx)

from uuid import uuid4

def add_ads(request):
    model = Ads()
    form: AdsForm  = AdsForm(request.POST,request.FILES,instance=model)
    media: TemporaryUploadedFile = request.FILES.get("photo")
    
    if form.is_valid():
        

        if media:
            media_type = media.content_type.split("/")[0]
            media.name = f"{uuid4()}.{media.name.split('.')[-1]}"
            im:FieldFile = form.instance.photo
            im.name = f"{uuid4()}.{media.name.split('.')[-1]}"
            if media_type == "image":
                form.instance.mode = 1
            elif media_type == "video":
                form.instance.mode = 2
            else:
                form.instance.mode = 0

            
        form.save()
        return redirect("all_ads")
        # pass
    else:
        print(form.errors)
    ctx = {
        "form":form,
        "ads_active":"active"

    }
    return render(request,"dashboard/ads_and_present/create_ads.html",ctx)

def send_ads(request,pk):
    ads = Ads.objects.get(pk=pk)
    try:
        requests.get(f"http://127.0.0.1:6002/send_ads", json={"data": {"id":ads.id}})
        messages.success(request,"Reklama barchaga yuborildi")
    except:
        messages.error(request,"Reklama yuborishda xatolik yuz berda qayta yuboring")
    return redirect("all_ads")


def delete_ads(request,pk):
    ads = Ads.objects.get(pk=pk)
    ads.delete()
    messages.warning(request,"Reklama o'chirildi")
    return redirect("all_ads")

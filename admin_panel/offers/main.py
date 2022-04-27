from django.shortcuts import render, redirect
import requests
from admin_panel.forms import OffersForm
from admin_panel.models import Ads, Aksiya
from django.contrib import messages
def all_offers(request):
    ads = Aksiya.objects.order_by("-id").all()
    ctx = {
        "ads":ads,
        "present_active":"active"
    }
    return render(request,"dashboard/offers/ads.html",ctx)

def add_offers(request):
    data = request.POST
    if request.method == "POST":
        name_uz, name_ru = data.get("name_uz"), data.get("name_ru")
        mode, caption = data.get("mode"), data.get("caption")
        mode = int(mode)
        media = request.FILES.get("media")

        new_aksiya = Aksiya.objects.create(name_uz=name_uz, name_ru=name_ru, mode=mode, caption=caption, media=media)
        return redirect("all_offers")
    
    return render(request,"dashboard/offers/create_ads.html")



def delete_offer(request,pk):
    ads = Aksiya.objects.get(pk=pk)
    ads.delete()
    messages.warning(request,"Reklama o'chirildi")
    return redirect("all_offers")

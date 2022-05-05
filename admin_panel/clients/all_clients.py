from datetime import datetime
from django.shortcuts import render,redirect
from django.contrib import messages
from admin_panel.models import Fillials, Support, User
import requests
def clients_list(request):
    fillials = Fillials.objects.all()
    clients = User.objects.order_by("-id").all()
    if request.POST:
        data = request.POST
        if data.get("fillial")!= "all":
            if data.get("from")and data.get("to"):
                clients = User.objects.filter(filial_id=data.get("fillial"),created_at__range=[data.get("from"),data.get("to")])
            elif data.get("from"):
                clients = User.objects.filter(filial_id=data.get("fillial"),created_at__gte=data.get("from"))
            elif data.get("to"):
                clients = User.objects.filter(filial_id=data.get("fillial"),created_at__lte=data.get("to"))

            else:
                clients = User.objects.filter(filial_id=data.get("fillial"))
        elif data.get("from")and data.get("to"):
            print("bbb",data.get("from"),data.get("to"))
            clients = User.objects.filter(created_at__range=[data.get("from"),data.get("to")]) 
        elif data.get("from"):
                clients = User.objects.filter(created_at__gte=data.get("from"))
        elif data.get("to"):
                clients = User.objects.filter(created_at__lte=data.get("to"))
    ctx = {"users_active":"active","clients":clients,"fillials":fillials}
    return render(request, 'dashboard/clients/list.html',ctx)




def send_telegram(request,pk):
    if request.method == 'POST':
        print(request.POST.get('id_name'))
        requests.get(f"http://127.0.0.1:6002/send_sms", json={"data": {
            "id":pk,
            "message":request.POST.get("id_name")
        }})
        messages.success(request,"Habaringiz Muvofaqiyatli yuborildi")
        return redirect("clients_list")
    ctx = {"users_active":"active"}
    return render(request, 'dashboard/clients/telegram.html',ctx)


def comments_list(request):
    comments = Support.objects.order_by("status").all()
    if request.POST:
        pk = request.POST["user"]
        comment_id = request.POST["comment"]
        try:
            requests.get(f"http://127.0.0.1:6002/send_sms", json={"data": {
                "id":pk,
                "message":request.POST.get("message")
            }})
            messages.success(request,"Habaringiz yuborildi")
            Support.objects.filter(id=comment_id).update(status=True)
        except:
            messages.error(request,"Xatolik yuz berdi qayta urinib ko'ring")
        return redirect("comments_list")
    ctx = {
        "comments":comments,"comment_active":"active"
    }
    return render(request,"dashboard/clients/comments.html",ctx)
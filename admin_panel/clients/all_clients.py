from django.shortcuts import render,redirect
from django.contrib import messages
from admin_panel.models import User
import requests
def clients_list(request):
    clients = User.objects.order_by("-id").all()
    ctx = {"users_active":"active","clients":clients}
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
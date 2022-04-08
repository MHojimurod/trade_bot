from django.shortcuts import render,redirect


def clients_list(request):
    return render(request, 'dashboard/clients/list.html')




def send_telegram(request,pk):
    if request.method == 'POST':
        print(request.POST.get('id_name'))
        return redirect("clients_list")
    return render(request, 'dashboard/clients/telegram.html')
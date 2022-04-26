import requests
from admin_panel.models import Busket, BusketItem, Operators
from django.shortcuts import redirect, render
def orders_list(request):
    if not request.user.is_superuser:
        operator = Operators.objects.get(user=request.user)
        if operator.is_have:
            order = Busket.objects.order_by('-id').filter(bis_ordered=True,status=1,actioner=operator).first()
            return redirect('one_order',order.id)
            
    orders = Busket.objects.filter(bis_ordered=True,status=0)
    data = []
    for i in orders:
        data.append(
            {
                "order":i,
                "items":BusketItem.objects.filter(busket=i)
        })

    print(data)
    ctx = {"orders": data,"order_active":"active"}
    return render(request, 'dashboard/orders/list.html', ctx)

 
def update_order_status(request,pk,status):
    order = Busket.objects.get(pk=pk)
    print(request.user)
    operator = Operators.objects.get(user=request.user)
    try:
        requests.get(f"http://localhost:8002/act", json={
            'order': order.id
        })
    except:
        pass
    if status == 1:
        order.status = 1
        order.actioner = operator
        operator.is_have = True
        operator.save()
        
        order.save()
        requests.get(f"http://localhost:6002/order_updated", json={
            'order': order.id,
            'status': 1
        })
        return redirect('one_order',pk)
    if status == 2:
        if request.POST:
            commet = request.POST.get('commet')
            order.comment = commet
            order.status = 2
            order.save()
            requests.get(f"http://localhost:6002/order_updated", json={
            'order': order.id,
            'status': 2
            })
            return redirect("order_list")
    if status == 3:
        order.status = 3
    

    order.save()
    return redirect("")


def one_order(request,pk):
    try:
        Operators.objects.filter(user=request.user).update(is_have=True)
    except:
        pass
    order = Busket.objects.get(pk=pk)
    items:BusketItem = BusketItem.objects.filter(busket=order)
    text = "" 
    for i in items:
        text += f"{i.product.name_uz}<br> {i.product.p + i.product.p*i.month.percent // 100/i.month.months}\n"


    ctx = {"order_active":"active","order":order,"text":text}
    return render(request, 'dashboard/orders/one_order.html',ctx)


def order_accepted(request):
    data = []
    if request.user.is_superuser:
        orders = Busket.objects.filter(bis_ordered=True, status=3)
        for i in orders:
            data.append(
                {
                    "order": i,
                    "items": BusketItem.objects.filter(busket=i)
                })
    else:
        orders = Busket.objects.filter(bis_ordered=True, status=3,actioner=Operators.objects.get(user=request.user))
        for i in orders:
            text = ""
            for j in BusketItem.objects.filter(busket=i):
                text+= f"""<b>{j.product.name_uz}</b><br>    • {j.product.price(j.month) // j.month.months} x {j.month.months} = {j.product.price(j.month)}<br>bir oylik narxi<br>    • {j.product.price(j.month) // j.month.months} x {j.count} = {j.product.price(j.month) //  j.month.months * j.count}<br><br>"""
            data.append(
                {
                    "order": i,
                    "items":text
                })


    print(data)
    ctx = {"orders": data, "order_active": "active"}
    return render(request, 'dashboard/orders/accepted.html', ctx)


def order_archive(request):
    data = []
    if request.user.is_superuser:
        orders = Busket.objects.filter(bis_ordered=True, status__in=[2,5])
        for i in orders:
            data.append(
                {
                    "order": i,
                    "items": BusketItem.objects.filter(busket=i)
                })
    else:
        orders = Busket.objects.filter(bis_ordered=True, status__in=[2,5],actioner=Operators.objects.get(user=request.user))
        for i in orders:
            data.append(
                {
                    "order": i,
                    "items": BusketItem.objects.filter(busket=i)
                })
        

    ctx = {"orders": data, "order_active": "active"}
    return render(request, 'dashboard/orders/archive.html', ctx)


def order_not_accepted(request):
    data = []
    if request.user.is_superuser:
        orders = Busket.objects.filter(bis_ordered=True, status=4)
        for i in orders:
            data.append(
                {
                    "order": i,
                    "items": BusketItem.objects.filter(busket=i)
                })
    else:
        orders = Busket.objects.filter(bis_ordered=True, status=4,actioner=Operators.objects.get(user=request.user))
        for i in orders:
            text = ""
            for j in BusketItem.objects.filter(busket=i):
                text+= f"""<b>{j.product.name_uz}</b>\n    • {j.product.price(j.month) // j.month.months} x {j.month.months} = {j.product.price(j.month)}\numumiy narxi\n    • {j.product.price(j.month) // j.month.months} x {j.count} = {j.product.price(j.month) //  j.month.months * j.count}\n\n"""


            data.append(
                {
                    "order": i,
                    "items": text
                })

    ctx = {"orders": data, "order_active": "active"}
    return render(request, 'dashboard/orders/reject.html', ctx)


def order_accept(request,pk):
    print("xxxxxxxx")
    order = Busket.objects.get(pk=pk)
    order.status = 3
    operator = Operators.objects.get(user=request.user)
    order.actioner = operator
    operator.is_have = False
    order.save()
    operator.save()
    requests.get(f"http://localhost:6002/order_updated", json={
            'order': order.id,
            'status': 3
        })
    return redirect('orders_list')


def order_not_accept(request, pk):
    order = Busket.objects.get(pk=pk)
    order.status = 4
    operator = Operators.objects.get(user=request.user)
    order.actioner = operator
    operator.is_have = False
    order.save()
    operator.save()
    requests.get(f"http://localhost:6002/order_updated", json={
            'order': order.id,
            'status': 4
        })
    return redirect('orders_list')




def reject_order(request, pk):

    request.user.is_have = False
    request.user.save()
    
    order = Busket.objects.get(pk=pk)
    order.status = 2
    order.actioner = Operators.objects.filter(user=request.user).first()
    order.save()
    try:
        requests.get(f"http://localhost:8002/act", json={
            'order': pk
        })
    except:
        pass
    requests.get(f"http://localhost:6002/order_updated", json={
            'order': order.id,
            'status': 2
        })
    return redirect('orders_list')
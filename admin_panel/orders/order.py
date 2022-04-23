from pyexpat.errors import messages
from admin_panel.models import Busket, BusketItem, Operators
from django.shortcuts import redirect, render
def orders_list(request):
    orders = Busket.objects.filter(is_ordered=True,status=0)
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

 
def update_order_status(request,pk):
    order = Busket.objects.get(pk=pk)
    if pk == 1:
        return redirect('accept_order')
    if pk == 2:
        if request.POST:
            commet = request.POST.get('commet')
            if commet:
                pass
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
    orders = Busket.objects.filter(is_ordered=True, status=3)
    data = []
    for i in orders:
        data.append(
            {
                "order": i,
                "items": BusketItem.objects.filter(busket=i)
            })

    print(data)
    ctx = {"orders": data, "order_active": "active"}
    return render(request, 'dashboard/orders/accepted.html', ctx)


def order_archive(request):
    orders = Busket.objects.filter(is_ordered=True, status=5)
    data = []
    for i in orders:
        data.append(
            {
                "order": i,
                "items": BusketItem.objects.filter(busket=i)
            })

    print(data)
    ctx = {"orders": data, "order_active": "active"}
    return render(request, 'dashboard/orders/archive.html', ctx)


def order_not_accepted(request):
    orders = Busket.objects.filter(is_ordered=True, status=4)
    data = []
    for i in orders:
        data.append(
            {
                "order": i,
                "items": BusketItem.objects.filter(busket=i)
            })

    print(data)
    ctx = {"orders": data, "order_active": "active"}
    return render(request, 'dashboard/orders/archive.html', ctx)


def order_accept(request,pk):
    order = Busket.objects.get(pk=pk)
    order.status = 3
    order.actioner = request.user
    order.save()
    return redirect('orders_list')


def order_not_accept(request, pk):
    order = Busket.objects.get(pk=pk)
    order.status = 4
    order.actioner = request.user
    order.save()
    return redirect('orders_list')




def reject_order(request, pk):
    request.user.is_have = False
    request.user.save()
    order = Busket.objects.get(pk=pk)
    order.status = 2
    order.actioner = request.user
    order.save()

    return redirect('orders_list')
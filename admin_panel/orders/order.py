from admin_panel.models import Busket, BusketItem
from django.shortcuts import redirect, render
def orders_list(request):
    orders = Busket.objects.filter(is_ordered=True)
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
    order = Busket.objects.get(pk=pk)
    items:BusketItem = BusketItem.objects.filter(busket=order)
    text = "" 
    for i in items:
        text += f"{i.product.name_uz}\n  {i.product.tan_price + i.product.tan_price*i.month.percent // 100/i.month.months}\n"


    ctx = {"order_active":"active","order":order,"text":text}
    return render(request, 'dashboard/orders/one_order.html',ctx)
    



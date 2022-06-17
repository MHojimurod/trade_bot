import requests
from admin_panel.models import Busket, BusketItem, Fillials, Operators, money
from django.shortcuts import redirect, render
from django.contrib import messages


def filter_text(request, status):
    orders = ""
    data = request.POST
    if data.get("fillial") != "all":
        if data.get("from") and data.get("to"):
            orders = Busket.objects.filter(bis_ordered=True, status=status, user__filial_id=data.get(
                "fillial"), order_time__gte=data.get("from"), order_time__lte=data.get("to"))
        elif data.get("from"):
            orders = Busket.objects.filter(bis_ordered=True, status=status, user__filial_id=data.get(
                "fillial"), order_time__gte=data.get("from"),)
        elif data.get("to"):
            orders = Busket.objects.filter(bis_ordered=True, status=status, user__filial_id=data.get(
                "fillial"), order_time__lte=data.get("to"))
        else:
            orders = Busket.objects.filter(
                bis_ordered=True, status=status, user__filial_id=data.get("fillial"))
    elif data.get("from") and data.get("to"):
        orders = Busket.objects.filter(bis_ordered=True, status=status, order_time__gte=data.get(
            "from"), order_time__lte=data.get("to"))
    elif data.get("from"):
        orders = Busket.objects.filter(
            bis_ordered=True, status=status, order_time__gte=data.get("from"))
    elif data.get("to"):
        orders = Busket.objects.filter(
            bis_ordered=True, status=status, order_time__lte=data.get("to"))
    else:
        orders = Busket.objects.filter(bis_ordered=True, status=status)
    return products_text(orders)


def filter_text_operator(request, status, actioner):
    orders = ""
    data = request.POST
    if data.get("fillial") != "all":
        if data.get("from") and data.get("to"):
            orders = Busket.objects.filter(bis_ordered=True, status=status, actioner=actioner, user__filial_id=data.get(
                "fillial"), order_time__gte=data.get("from"), order_time__lte=data.get("to"))
        elif data.get("from"):
            orders = Busket.objects.filter(fbis_ordered=True, status=status, actioner=actioner, user__filial_id=data.get(
                "fillial"), order_time__gte=data.get("from"),)
        elif data.get("to"):
            orders = Busket.objects.filter(bis_ordered=True, status=status, actioner=actioner, user__filial_id=data.get(
                "fillial"), order_time__lte=data.get("to"))
        else:
            orders = Busket.objects.filter(
                bis_ordered=True, status=status, actioner=actioner, user__filial_id=data.get("fillial"))
    elif data.get("from") and data.get("to"):
        orders = Busket.objects.filter(bis_ordered=True, status=status, actioner=actioner, order_time__gte=data.get(
            "from"), order_time__lte=data.get("to"))
    elif data.get("from"):
        orders = Busket.objects.filter(
            bis_ordered=True, status=status, actioner=actioner, order_time__gte=data.get("from"))
    elif data.get("to"):
        orders = Busket.objects.filter(
            bis_ordered=True, status=status, actioner=actioner, order_time__lte=data.get("to"))
    else:
        orders = Busket.objects.filter(
            bis_ordered=True, status=status, actioner=actioner)
    return products_text(orders)


def products_text(orders):
    data = []
    for i in orders:
        text = ""
        total = 0
        to_month = 0
        for j in BusketItem.objects.filter(busket=i):
            total_price = j.product.price(j.month) * j.count
            text += f"<b>{j.product.name_uz}</b><br>      {money(total_price//j.month.months)} x {j.month.months} oy x {j.count} ta = {money(total_price)} so'm<br>"
            total += total_price
            to_month += total_price//j.month.months
        text += f"<b>Bir oylik to'lov:</b> {money(to_month)} so'm<br>"
        text += f"<b>Umumiy narx:</b>{ money(total)} so'm<br>"

        data.append(
            {
                "order": i,
                "items": text
            })
    return data


def orders_list(request):
    fillials = Fillials.objects.all()
    orders = ""
    fillial = ""
    if not request.user.is_superuser:
        operator = Operators.objects.get(user=request.user)
        if operator.is_have:
            order = Busket.objects.order_by(
                '-id').filter(bis_ordered=True, status=1, actioner=operator).first()
            return redirect('one_order', order.id)

    orders = Busket.objects.filter(bis_ordered=True, status=0)
    data = products_text(orders)
    filter_active_filial = request.POST.get("fillial")
    if request.POST:
        data = filter_text(request, 0)
    from_date = request.POST.get("from")
    to_date = request.POST.get("to")
    ctx = {
        "orders": data,
        "order_active": "active",
        "list_active": "active",
        "menu_open": "open",
        "fillials": fillials,
        "fillial": fillial,
        "from_date":from_date,
        "to_date":to_date,
        "filter_active_filial": int(filter_active_filial) if not filter_active_filial in ('all', None) else 0,

    }
    return render(request, 'dashboard/orders/list.html', ctx)


def update_order_status(request, pk, status):
    if not request.user.is_superuser:
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
            return redirect('one_order', pk)
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
                messages.warning(request, "Buyurtma Rad etildi")
                return redirect("order_list")
        if status == 3:
            order.status = 3

        order.save()
        return redirect("")
    else:
        messages.error(request, "Kechirasiz siz Operator emassiz")
        return redirect("orders_list")


def one_order(request, pk):
    try:
        Operators.objects.filter(user=request.user).update(is_have=True)
    except:
        pass
    order = Busket.objects.get(pk=pk)
    order_1 = Busket.objects.filter(pk=pk)
    data = products_text(order_1)

    ctx = {"order_active": "active", "order": order, "text": data[0]}
    return render(request, 'dashboard/orders/one_order.html', ctx)


def order_accepted(request):
    fillials = Fillials.objects.all()
    data = ""

    if request.user.is_superuser:
        orders = Busket.objects.filter(bis_ordered=True, status=3)
        data = products_text(orders)
        if request.POST:
            data = filter_text(request, 3)
    else:
        orders = Busket.objects.filter(
            bis_ordered=True, status=3, actioner=Operators.objects.get(user=request.user))
        data = products_text(orders)
        if request.POST:
            data = filter_text_operator(
                request, 3, Operators.objects.get(user=request.user))
    # get fillial
    filter_active_filial = request.POST.get("fillial")
    from_date = request.POST.get("from")
    to_date = request.POST.get("to")

    ctx = {
        "orders": data,
        "order_active": "active",
        "accept_active": "active",
        "menu_open": "open",
        "fillials": fillials,
        "from_date":from_date,
        "to_date":to_date,
        "filter_active_filial": int(filter_active_filial) if not filter_active_filial in ('all', None)  else 0,
    }
    return render(request, 'dashboard/orders/accepted.html', ctx)


def order_archive(request):
    fillials = Fillials.objects.all()
    data = ""
    if request.user.is_superuser:
        orders = Busket.objects.filter(bis_ordered=True, status__in=[2, 5])
        data = products_text(orders)
        if request.POST:
            data = request.POST
            if data.get("fillial") != "all":
                if data.get("from") and data.get("to"):
                    orders = Busket.objects.filter(bis_ordered=True, status__in=[2, 5], user__filial_id=data.get(
                        "fillial"), order_time__gte=data.get("from"), order_time__lte=data.get("to"))
                elif data.get("from"):
                    orders = Busket.objects.filter(fbis_ordered=True, status__in=[
                                                   2, 5], user__filial_id=data.get("fillial"), order_time__gte=data.get("from"),)
                elif data.get("to"):
                    orders = Busket.objects.filter(bis_ordered=True, status__in=[
                                                   2, 5], user__filial_id=data.get("fillial"), order_time__lte=data.get("to"))
                else:
                    orders = Busket.objects.filter(bis_ordered=True, status__in=[
                                                   2, 5], user__filial_id=data.get("fillial"))
            elif data.get("from") and data.get("to"):
                orders = Busket.objects.filter(bis_ordered=True, status__in=[
                                               2, 5], order_time__gte=data.get("from"), order_time__lte=data.get("to"))
            elif data.get("from"):
                orders = Busket.objects.filter(bis_ordered=True, status__in=[
                                               2, 5], order_time__gte=data.get("from"))
            elif data.get("to"):
                orders = Busket.objects.filter(bis_ordered=True, status__in=[
                                               2, 5], order_time__lte=data.get("to"))
            else:
                orders = Busket.objects.filter(
                    bis_ordered=True, status__in=[2, 5])
            data = products_text(orders)

    else:
        actioner = Operators.objects.get(user=request.user)
        orders = Busket.objects.filter(bis_ordered=True, status__in=[
                                       2, 5], actioner=actioner)
        data = products_text(orders)
        data = request.POST
        if data.get("fillial") != "all":
            if data.get("from") and data.get("to"):
                orders = Busket.objects.filter(bis_ordered=True, status__in=[2, 5], actioner=actioner, user__filial_id=data.get(
                    "fillial"), order_time__gte=data.get("from"), order_time__lte=data.get("to"))
            elif data.get("from"):
                orders = Busket.objects.filter(fbis_ordered=True, status__in=[
                                               2, 5], actioner=actioner, user__filial_id=data.get("fillial"), order_time__gte=data.get("from"),)
            elif data.get("to"):
                orders = Busket.objects.filter(bis_ordered=True, status__in=[
                                               2, 5], actioner=actioner, user__filial_id=data.get("fillial"), order_time__lte=data.get("to"))
            else:
                orders = Busket.objects.filter(bis_ordered=True, status__in=[
                                               2, 5], actioner=actioner, user__filial_id=data.get("fillial"))
        elif data.get("from") and data.get("to"):
            orders = Busket.objects.filter(bis_ordered=True, status__in=[
                                           2, 5], actioner=actioner, order_time__gte=data.get("from"), order_time__lte=data.get("to"))
        elif data.get("from"):
            orders = Busket.objects.filter(bis_ordered=True, status__in=[
                                           2, 5], actioner=actioner, order_time__gte=data.get("from"))
        elif data.get("to"):
            orders = Busket.objects.filter(bis_ordered=True, status__in=[
                                           2, 5], actioner=actioner, order_time__lte=data.get("to"))
        else:
            orders = Busket.objects.filter(bis_ordered=True, status__in=[
                                           2, 5], actioner=actioner)
        data = products_text(orders)
    filter_active_filial = request.POST.get("fillial")
    from_date = request.POST.get("from")
    to_date = request.POST.get("to")
    ctx = {
        "orders": data,
        "order_active": "active",
        "archive_active": "active",
        "menu_open": "open",
        "fillials": fillials,
        "from_date":from_date,
        "to_date":to_date,
        "filter_active_filial": int(filter_active_filial) if not filter_active_filial in ('all', None)  else 0,
    }
    return render(request, 'dashboard/orders/archive.html', ctx)


def order_not_accepted(request):
    fillials = Fillials.objects.all()
    data = []
    if request.user.is_superuser:
        orders = Busket.objects.filter(bis_ordered=True, status=4)
        data = products_text(orders)
        if request.POST:
            data = filter_text(request, 4)
    else:
        orders = Busket.objects.filter(
            bis_ordered=True, status=4, actioner=Operators.objects.get(user=request.user))
        data = products_text(orders)
        if request.POST:
            data = filter_text(
                request, 4, Operators.objects.get(user=request.user))
    filter_active_filial = request.POST.get("fillial")
    from_date = request.POST.get("from")
    to_date = request.POST.get("to")

    ctx = {
        "orders": data,
        "order_active": "active",
        "not_accept_active": "active",
        "menu_open": "open",
        "fillials": fillials,
        "from_date":from_date,
        "to_date":to_date,
        "filter_active_filial": int(filter_active_filial) if not filter_active_filial in ('all', None)  else 0,
    }
    return render(request, 'dashboard/orders/reject.html', ctx)


def order_accept(request, pk):
    if not request.user.is_superuser:
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
        messages.success(request, "Maxsulot tasdiqlandi")
    else:
        messages.error(request, "Kechirasiz siz Operator emassiz")
    return redirect('orders_list')


def order_not_accept(request, pk):
    if not request.user.is_superuser:
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
        messages.success(request, "Maxsulot rad etildi")
    else:
        messages.error(request, "Kechirasiz siz Operator emassiz")
    return redirect('orders_list')


def reject_order(request, pk):

    if not request.user.is_superuser:
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
        messages.warning(request, "Maxsulot qabul qilinmadi")
    else:
        messages.error(request, "Kechirasiz siz Operator emassiz")
    return redirect('orders_list')


def archive_order(request, pk):
    if not request.user.is_superuser:
        order = Busket.objects.get(pk=pk)
        op = Operators.objects.filter(user=request.user)

        order.actioner = op.first()
        op.update(is_have=False)
        order.status = 5
        order.save()
        messages.warning(request, "Maxsulot arxivga joylandi")
    else:
        messages.error(request, "Kechirasiz siz Operator emassiz")
    return redirect('orders_list')

from django.shortcuts import render, redirect
from admin_panel.forms import FillialsForm
from admin_panel.models import Fillials
from django.contrib import messages


def create_fillial(request):
    model = Fillials()
    form = FillialsForm(request.POST,instance=model)
    if form.is_valid():
        form.save()
        return redirect('/fillials/list')
    ctx = {'form': form, "fillial_active":"active"}
    return render(request, 'dashboard/fillials/create.html', ctx)

def list_fillial(request):
    if request.POST:
        data = request.POST
        if len(data.getlist("results"))>0:
            if data["action"] == "active":
                for i in data.getlist("results"):
                    Fillials.objects.filter(id=i).update(active=True)
            if data["action"] == "not_active":
                for i in data.getlist("results"):
                    Fillials.objects.filter(id=i).update(active=False)
            if data["action"] == "delete":
                for i in data.getlist("results"):
                    Fillials.objects.filter(id=i).delete()
            return redirect('list_fillial')
        else:
            messages.error(request,"Siz hech narsa tanlamadingiz")
            return redirect('list_fillial')

    fillials = Fillials.objects.all()
    ctx = {'fillials': fillials, "fillial_active":"active"}
    return render(request, 'dashboard/fillials/list.html', ctx)

def edit_fillial(request, id):
    fillial = Fillials.objects.get(id=id)
    form = FillialsForm(request.POST or None,instance=fillial)
    if form.is_valid():
        form.save()
        return redirect('/fillials/list')
    ctx = {'form': form,"data":fillial, "fillial_active":"active"}
    return render(request, 'dashboard/fillials/edit.html', ctx)

def delete_fillial(request, id):
    fillial = Fillials.objects.get(id=id)
    fillial.delete()
    return redirect('/fillials/list')

def one_fillial(request,pk):
    fillial = Fillials.objects.get(pk=pk)
    ctx = {"fillial":fillial, "fillial_active":"active"}
    return render(request,"dashboard/fillials/one_fillial.html",ctx)

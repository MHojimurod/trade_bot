from django.shortcuts import render, redirect
from admin_panel.forms import FillialsForm
from admin_panel.models import Fillials



def create_fillial(request):
    model = Fillials()
    form = FillialsForm(request.POST,instance=model)
    if form.is_valid():
        form.save()
        return redirect('/fillials/list')
    ctx = {'form': form}
    return render(request, 'dashboard/fillials/create.html', ctx)

def list_fillial(request):
    fillials = Fillials.objects.all()
    ctx = {'fillials': fillials}
    return render(request, 'dashboard/fillials/list.html', ctx)

def edit_fillial(request, id):
    fillial = Fillials.objects.get(id=id)
    form = FillialsForm(request.POST or None,instance=fillial)
    if form.is_valid():
        form.save()
        return redirect('/fillials/list')
    ctx = {'form': form,"data":fillial}
    return render(request, 'dashboard/fillials/edit.html', ctx)

def delete_fillial(request, id):
    fillial = Fillials.objects.get(id=id)
    fillial.delete()
    return redirect('/fillials/list')
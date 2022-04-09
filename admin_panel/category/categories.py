from calendar import c
from pyexpat import model
from django.shortcuts import render, redirect
from admin_panel.forms import CategoryForm
from django.contrib import messages
from admin_panel.models import Category


def list_category(request):
    category = Category.objects.filter(parent_id=None)
    print(category)
    ctx = {'category': category, "category_active":"active"}
    return render(request, 'dashboard/category/list.html', ctx)



def create_category(request):
    model = Category()
    form = CategoryForm(request.POST,instance=model)
    print(request.POST)
    if request.POST:
        if form.is_valid():
            form.save()
            messages.success(request, "Muaffaqiyatli yaratildi!")
            return redirect('/category/list')
        else:
            messages.error(request,"Ma'lumotlarni to'g'ri kiriting")
        
    ctx = {'form': form, "category_active":"active"}
    

    return render(request, 'dashboard/category/create.html',ctx)


def edit_category(request, pk):
    category = Category.objects.get(id=pk)
    form = CategoryForm(request.POST or None,instance=category)
    if form.is_valid():
        form.save()
        messages.success(request, "Muaffaqiyatli o'zgartirildi!")
        return redirect('/category/list')

    ctx = {'form': form,"data":category, "category_active":"active"}
    messages.error(request,"Ma'lumotlarni to'g'ri kiriting")
    return render(request, 'dashboard/category/edit.html', ctx)



def delete_category(request, pk):
    category = Category.objects.get(id=pk)
    category.delete()
    messages.warning(request,"Ma'lumotlarni o'chirildi")
    return redirect('/category/list')
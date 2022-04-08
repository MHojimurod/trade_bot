from calendar import c
from pyexpat import model
from django.shortcuts import render, redirect
from admin_panel.forms import CategoryForm, SubCategoryForm
from django.db.models import Q
from admin_panel.models import Category


def list_sub_category(request,pk):
    category = Category.objects.filter(parent_id=pk)
    first_category =  Category.objects.filter(id=pk).first()
    ctx = {'sub_category': category,"first_category": first_category, "category_active":"active"}
    return render(request, 'dashboard/sub_category/list.html', ctx)



def create_sub_category(request,pk):
    model = Category()

    form = SubCategoryForm(request.POST,instance=model)
    if form.is_valid():
        form.save()
        print(form.cleaned_data)
        return redirect(f'/sub_category/list/{pk}')
    ctx = {'form': form,"category": pk, "category_active":"active"}
    return render(request, 'dashboard/sub_category/create.html',ctx)



def edit_sub_category(request, pk):
    category = Category.objects.get(id=pk)
    form = CategoryForm(request.POST or None,instance=category)
    if form.is_valid():
        data = form.save()
        return redirect(f'/sub_category/list/{data.parent_id}')
    ctx = {'form': form,"data":category, "category_active":"active"}
    return render(request, 'dashboard/sub_category/edit.html', ctx)



def delete_sub_category(request, pk):
    category = Category.objects.get(id=pk)
    data = category.parent_id
    category.delete()
    return redirect(f'/sub_category/list/{data}')
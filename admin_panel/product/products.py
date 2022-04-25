from calendar import c
from multiprocessing import parent_process
from pyexpat import model
from pyexpat.errors import messages
import re
from django.shortcuts import render, redirect
from admin_panel.forms import CategoryForm, ProductForm, SubCategoryForm
from django.db.models import Q
from admin_panel.models import Category, Color, Product
from django.contrib import messages

def list_product(request,pk):
    if request.method == "POST":
        data = request.POST
        if len(data.getlist("results"))>0:
            if data["action"] != "delete":
                for i in data.getlist("results"):
                    product = Product.objects.get(id=i)
                    product.color = Color.objects.get(id=int(data["action"]))
                    product.save()
            if data["action"] == "delete":
                for i in data.getlist("results"):
                    Product.objects.filter(id=i).delete()
            messages.success(request,"Muvafaqqiyatli o'zgartirildi")
            
                
        else:
            messages.error(request,"Siz hech narsa tanlamadingiz")
        return redirect(f'/product/list/{pk}')

                
    products = Product.objects.filter(category_id=pk)
    sub = Category.objects.filter(id=pk).first()
    main_category = Category.objects.filter(pk=sub.parent_id).first()
    ctx = {'products': products,"main_category": main_category,"sub":sub,"category_active":"active"}
    return render(request, 'dashboard/products/list.html', ctx)



def create_product(request,pk):
    sub = Category.objects.filter(id=pk).first()
    main_category = Category.objects.filter(id=sub.parent_id).first()
    model = Product()
    form = ProductForm(request.POST,request.FILES,instance=model)
    print(form.errors)
    if form.is_valid():
        form.save()
        return redirect(f'/product/list/{pk}')
    ctx = {'form': form,"category": pk,"main_category": main_category,"sub":sub,"category_active":"active"}
    return render(request, 'dashboard/products/create.html',ctx)


def edit_product(request, pk):
    
    category = Product.objects.get(id=pk)
    sub = Category.objects.filter(id=category.category_id).first()
    main_category = Category.objects.filter(id=sub.parent_id).first()
    form = ProductForm(request.POST or None,request.FILES or None,instance=category)
    if form.is_valid():
        form.save()
        return redirect(f'/product/list/{sub.id}')
    ctx = {'form': form,"data":category,"category_active":"active","sub":sub,"main_category": main_category}
    return render(request, 'dashboard/products/edit.html', ctx)



def delete_product(request, pk):
    category = Product.objects.get(id=pk)
    data = category.parent_id
    category.delete()
    return redirect(f'/product/list/{data}')


def one_product(request, pk):
    product = Product.objects.get(pk=pk)
    sub:Category = Category.objects.filter(id=product.category_id).first()
    main_category:Category = Category.objects.filter(id=sub.parent_id).first()
    ctx = {
        "product": product,
        "category_active":"active",
        "main_category": main_category,
        "sub":sub
    }
    return render(request, 'dashboard/products/one_product.html', ctx)
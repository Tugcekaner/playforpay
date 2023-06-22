
import random
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.urls import reverse

# Create your views here.
def indexPage(request):
    categories=Category.objects.all()
    product=Product.objects.all()

    context={
        'categories':categories,
        'product':product
    }

    return render(request,'index.html',context)

def detailPage(request,id):

    categories = get_object_or_404(Category, id=id)
    products = categories.product_set.all()

    other_categories = Category.objects.exclude(id=id)
    random_categories = random.sample(list(other_categories), 12)

    context={
        'categories':categories,
        'products':products,
        'random_categories':random_categories,
    }
    return render(request, 'detail.html', context)

def productDetailPage(request,id):

    product = get_object_or_404(Product, id=id)

    context={
        'product':product
    }
    return render(request, 'product_detail.html', context)

def productsPage(request):
    categories=Category.objects.all()
    products=Product.objects.all()
    context={
        'categories':categories,
        'products':products
    }
    return render(request,'products.html',context)

def buyerPage(request):
    categories=Category.objects.all()
    products=Product.objects.all()
    users=User.objects.all()

    context={
        'categories':categories,
        'products':products,
        'users':users
    }
    return render(request,'buyers.html',context)

import random
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.urls import reverse

# Create your views here.

# * Ana Sayfa
def indexPage(request):
    categories=Category.objects.all()
    product=Product.objects.all()

    context={
        'categories':categories,
        'product':product
    }

    return render(request,'index.html',context)

# * Oyun detay sayfası
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

# * Ürün detay sayfası
def productDetailPage(request,id):

    product = get_object_or_404(Product, id=id)

    context={
        'product':product
    }
    return render(request, 'product_detail.html', context)

# * ürünler sayfası
def productsPage(request):
    categories=Category.objects.all()
    products=Product.objects.all()
    context={
        'categories':categories,
        'products':products
    }
    return render(request,'products.html',context)

# * satıcı sayfası
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

# * oyuncular sayfası
def playerPage(request):
    categories=Category.objects.all()
    players=Player.objects.all()

    context={
        'categories':categories,
        'players':players
    }
    return render(request,'players.html',context)

# * oyuncular detay sayfası
def playerDetailPage(request,id):
    
    player = get_object_or_404(Player, id=id)

    context={
        'player': player
    }
    return render(request, 'player_detail.html', context)


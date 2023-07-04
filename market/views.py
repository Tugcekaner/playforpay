
import random
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User


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

# * Hakkımızda sayfası
def aboutPage(request):
    return render(request,'about.html')

# * SSS sayfası
def faqPage(request):
    return render(request,'faq.html')


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
def sellerPage(request):
    categories=Category.objects.all()
    products=Product.objects.all()
    users=User.objects.all()

    context={
        'categories':categories,
        'products':products,
        'users':users
    }
    return render(request,'sellers.html',context)

# * satıcıya ait ürünler sayfası
def sellerProductPage(request,id):
    user=User.objects.get(id=id)
    products=Product.objects.filter(user=user)

    other_sellers = User.objects.exclude(id=id)
    random_sellers = random.sample(list(other_sellers), 6)

    context={
        'products': products,
        'random_sellers': random_sellers
    }
    return render(request,'seller_product.html',context)


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

# * ürünlerim sayfası
def myProductPage(request):
    products=Product.objects.filter(user=request.user)
    if request.method == "POST":
        title=request.POST.get("title")
        price=request.POST.get("price")
        stok = request.POST.get("stok")
        text = request.POST.get("text")
        image = request.FILES.get("image")
        productid = request.POST.get("productid")
        product = products.get(id=productid)  # değiştirilcek ürün
        product.title = title
        product.price = price
        product.stok = stok
        product.text = text
        if image is not None:
            product.image = image
        product.save()
        return redirect("myproducts")

    context = {
        "products": products,
    }
    return render(request,"myproduct.html",context)


# * ürünlerimden ürün silme
def delProduct(request, id=None):
    if id is not None:
        product = Product.objects.get(id=id)
        product.delete()
    else:
        messages.warning(request, "Ürün bulunamadı!")
    return redirect("myproducts")

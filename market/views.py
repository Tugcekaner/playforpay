
import random
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.

# * Ana Sayfa
def indexPage(request):
    shop=Shoping.objects.all()
    categories=Category.objects.all()
    product=Product.objects.all()

    context={
        'categories':categories,
        'product':product,
        'shop':shop
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

    if request.method == "POST":
        if request.user.is_authenticated:
            submit = request.POST.get("submit")
            if submit == "shopForm":
                piece = request.POST.get("piece")
            
                if 1 <= int(piece) <= int(product.stok): 
                    if not Shoping.objects.filter(user=request.user, product=product).exists():
                        shop = Shoping(user=request.user, product=product, piece=piece)
                    else:
                        shop = Shoping.objects.filter(user=request.user, product=product).get()
                        if (int(shop.piece)+int(piece)) <= int(product.stok):
                            shop.piece += int(piece)
                        else:
                            messages.warning(request, 'maximum ürün adetini aştınız. Ekleyebileceğiniz ürün adeti: '+str(int(product.stok)-int(shop.piece)))
                    shop.save()
                    return redirect('shoppage')
            else:
               messages.warning(request, 'Stok sayısını aştınız.')

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

    if request.method == "POST":
        if request.user.is_authenticated:
            submit = request.POST.get("submit")
            if submit == "shopForm":
                piece = request.POST.get("piece")
                
                if 1 <= int(piece) <= int(player.stok):
                    messages.success(request, 'Oyun isteği gönderildi.')
                else:
                    messages.warning(request, 'Stok sayısını aştınız.')

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

# * Ürün ekleme sayfası
def addProductPage(request):
    categories=Category.objects.all()
    types=Type.objects.all()

    if request.method == "POST":
        title = request.POST.get("title")
        price = request.POST.get("price")
        stok = request.POST.get("stok")
        text = request.POST.get("text")
        image = request.FILES.get("image")
        slugcate = request.POST.get("category")
        category = categories.get(slug=slugcate)
        slugtype = request.POST.get("type")
        type = types.get(slug=slugtype)

        product = Product(title=title, stok=stok, category=category, price=price,
                    text=text,type=type, image=image, user=request.user)

        product.save()
        return redirect("myproducts")

    context={
        'categories':categories,
        'types':types,
    }
    return render(request,'addProduct.html',context)

# * sepet sayfası
def shoppingPage(request):
    shop=Shoping.objects.filter(user=request.user)
    total_price = 0

    for i in shop:
        total_price += i.price

    if request.method == "POST":
        index = 0
        for k,v in request.POST.items():
            if "csrfmiddlewaretoken" not in k and "submit" not in k:
                if index%2 == 0:
                    shoping = shop.get(id=v)
                    shoping.save()
                elif index%2 == 1:
                    if int(shoping.product.stok) >= int(v):
                        shoping.piece = v
                        shoping.save()
                    else:
                        messages.warning(request, shoping.product.title+' ürünün stok sayısını aştınız. max:'+ str(shoping.product.stok))
            index +=1
        shoping.save()
        return redirect('shoppage')

    context = {
      "shop":shop,
      "total_price": total_price,
    }
    return render(request,'shopping.html',context)

# * sepetten ürün silme
def shopDelete(request, id):
   shoping = Shoping.objects.filter(id=id)
   if shoping.exists():
      shoping = shoping.get()
   shoping.delete()
   return redirect("shoppage")


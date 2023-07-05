
import random
from django.shortcuts import render,redirect,get_object_or_404
from .models import *
from django.contrib.auth.models import User
import iyzipay
import json
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import requests
from django.contrib import messages
import pprint

# ? pip install iyzipay
# ? pip install requests
# * ödeme 
api_key = 'sandbox-DCEdEAASjyyBiJReO7tOlnLrSIzmN3Av'
secret_key = 'sandbox-4XjmVhCoO0vl1ckfZ4rVhj1Jcfi7gCsE'
base_url = 'sandbox-api.iyzipay.com'
# ! canlıya alındığında sandbox- kısımlar silinecek
# ! gerçek ödeme alabilmek için

options = {
    'api_key': api_key,
    'secret_key': secret_key,
    'base_url': base_url
}
sozlukToken = list()

def payment(request):
    context = dict()
# * satın alan kişinin bilgilerini ödemeler için dinamik hale getirme
# * buyerUser = request.user


    buyer={
        'id': 'BY789',
        'name': 'John',
        'surname': 'Doe',
        'gsmNumber': '+905350000000',
        'email': 'email@email.com',
        'identityNumber': '74300864791',
        'lastLoginDate': '2015-10-05 12:43:35',
        'registrationDate': '2013-04-21 15:12:09',
        'registrationAddress': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'ip': '85.34.78.112',
        'city': 'Istanbul',
        'country': 'Turkey',
        'zipCode': '34732'
    }

    address={
        'contactName': 'Jane Doe',
        'city': 'Istanbul',
        'country': 'Turkey',
        'address': 'Nidakule Göztepe, Merdivenköy Mah. Bora Sok. No:1',
        'zipCode': '34732'
    }

    basket_items=[
        {
            'id': 'BI101',
            'name': 'Binocular',
            'category1': 'Collectibles',
            'category2': 'Accessories',
            'itemType': 'PHYSICAL',
            'price': '0.3'
        },
        {
            'id': 'BI102',
            'name': 'Game code',
            'category1': 'Game',
            'category2': 'Online Game Items',
            'itemType': 'VIRTUAL',
            'price': '0.5'
        },
        {
            'id': 'BI103',
            'name': 'Usb',
            'category1': 'Electronics',
            'category2': 'Usb / Cable',
            'itemType': 'PHYSICAL',
            'price': '0.2'
        }
    ]
# ! checkoutformcontent hatası alıyorsan price kısmını incele,hata oradadır
    request={
        'locale': 'tr',
        'conversationId': '123456789',
        'price': '1',
        'paidPrice': '1.2',
        'currency': 'TRY',
        'basketId': 'B67832',
        'paymentGroup': 'PRODUCT',
        # * callback url önemli, kendi url linkini koymalısın
        "callbackUrl": "http://127.0.0.1:8000/result/",
        # * taksit seçenekleri kısmı
        "enabledInstallments": ['2', '3', '6', '9','12'],
        'buyer': buyer,
        'shippingAddress': address,
        'billingAddress': address,
        'basketItems': basket_items,
        # 'debitCardAllowed': True
    }

    checkout_form_initialize = iyzipay.CheckoutFormInitialize().create(request, options)

    #print(checkout_form_initialize.read().decode('utf-8'))
    page = checkout_form_initialize
    header = {'Content-Type': 'application/json'}
    content = checkout_form_initialize.read().decode('utf-8')
    json_content = json.loads(content)
    print(type(json_content))
    print(json_content["checkoutFormContent"])
    print("************************")
    print(json_content["token"])
    print("************************")
    sozlukToken.append(json_content["token"])
# * httpresponse kısmında mobil uyum için değişiklik yaptık
    return HttpResponse(f'<div id="iyzipay-checkout-form" class="responsive">{json_content["checkoutFormContent"]}</div>')


@require_http_methods(['POST'])
@csrf_exempt
def result(request):
    context = dict()

    url = request.META.get('index')

    request = {
        'locale': 'tr',
        'conversationId': '123456789',
        'token': sozlukToken[0]
    }
    checkout_form_result = iyzipay.CheckoutForm().retrieve(request, options)
    print("************************")
    print(type(checkout_form_result))
    result = checkout_form_result.read().decode('utf-8')
    print("************************")
    print(sozlukToken[0])   # Form oluşturulduğunda 
    print("************************")
    print("************************")
    sonuc = json.loads(result, object_pairs_hook=list)
    #print(sonuc[0][1])  # İşlem sonuç Durumu dönüyor
    #print(sonuc[5][1])   # Test ödeme tutarı
    print("************************")
    for i in sonuc:
        print(i)
    print("************************")
    print(sozlukToken)
    print("************************")
    if sonuc[0][1] == 'success':
        context['success'] = 'Başarılı İŞLEMLER'
        return HttpResponseRedirect(reverse('success'), context)

    elif sonuc[0][1] == 'failure':
        context['failure'] = 'Başarısız'
        return HttpResponseRedirect(reverse('failure'), context)

    return HttpResponse(url)



def success(request):
    context = dict()
    context['success'] = 'İşlem Başarılı'

    template = 'ok.html'
    return render(request, template, context)


def fail(request):
    context = dict()
    context['fail'] = 'İşlem Başarısız'

    template = 'fail.html'
    return render(request, template, context)




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
    products = Shoping.objects.filter(user=request.user,paymentCheck=False)
    shop=Shoping.objects.filter(user=request.user)
    total_price = 0

    for i in shop:
        total_price += i.price

    if request.method == "POST":
        if 'odeme' in request.POST:
            odeme = odeme.objects.create(
                user = request.user,
                total = total_price,
            )
            odeme.products.add(*products)
            odeme.save()
            return redirect('payment')
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


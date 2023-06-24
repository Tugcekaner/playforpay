from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
# from django.db.models import Count

# Create your views here.


# def loginPage(request):

#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#     user = authenticate(username=username, password=password) # bulamazsa None

#     context = {}

#     if request.user.is_authenticated:
#         context.update({"profile": UserInfo.objects.get(user=request.user)})
#     return render(request,'user/login.html',context)

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username,password=password)

        context = {}

        if user is not None:
            login(request, user)
            context.update({"profile": UserInfo.objects.get(username=request.user.username)})
            return redirect('index')
        else:
            context["login_error"] = "Geçersiz kullanıcı adı veya şifre."

    context = {}
    if request.user.is_authenticated:
        context.update({"profile": UserInfo.objects.get(user=request.user)})

    return render(request, 'login.html',context)


def registerPage(request):

    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 == password2:
            if not User.objects.filter(username=username).exists():
                if not User.objects.filter(email=email).exists():
                    user = User.objects.create_user(
                        username=username, email=email)

                    # userinfo = UserInfo(user=user)
                    # userinfo.save()
                    messages.success(request, 'Kaydınız başarıyla oluşturuldu..')
                    return redirect("login")
                else:
                    messages.warning(request, 'Bu mail zaten kullanılıyor!!')
                    return redirect("login")
            else:
                messages.warning(
                    request, 'Bu kullanıcı adı daha önceden alınmış!!')
                return redirect("login")
        else:
            messages.warning(request, 'Şifreler aynı değil!!')
            return redirect("register")

    context = {
        'user':user,
    }

    if request.user.is_authenticated:
        context.update({"profile": UserInfo.objects.get(user=request.user)})
    return render(request,'register.html',context)

def logoutUser(request):
   logout(request)
   return redirect("login")
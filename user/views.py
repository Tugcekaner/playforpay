from django.shortcuts import render, redirect
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
# from django.contrib import messages
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
      
        user = authenticate(username=username, password=password)  # bulamazsa None

        context = {}

        if user is not None:
            login(request, user)
            context.update({"profile": User.objects.get(username=request.user.username)})
            return redirect('index')
        else:
            # Kullanıcı kimlik doğrulaması başarısız oldu
            context["login_error"] = "Geçersiz kullanıcı adı veya şifre."

    return render(request, 'login.html')




def registerPage(request):
    return render(request,'register.html')

def logoutUser(request):
   logout(request)
   return redirect("login")
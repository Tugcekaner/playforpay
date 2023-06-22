"""
URL configuration for playforpay project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from market.views import *
from user.views import *

urlpatterns = [
    path('admin/', admin.site.urls),

    # * market
    path('',indexPage, name='index'),
    path('products/',productsPage, name='products'),
    path('buyers/',buyerPage, name='buyers'),
    path('detail/<id>',detailPage, name='detail'),
    path('product_detail/<id>',productDetailPage, name='product_detail'),

    # *user
    path('login/',loginPage, name='login'),
    path('register/',registerPage, name='register'),
    path('logout', logoutUser, name='logoutUser'), # çıkış

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

from django.contrib import admin
from.models import *

class SepetAdmin(admin.ModelAdmin):
    list_display = ['user','product','piece','price','paymentCheck']
    list_filter = ['user','product','paymentCheck']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'total', 'paymentDate','paymentCheck']
    list_filter = ['user','paymentCheck']

class ProductAdmin(admin.ModelAdmin):
    list_display = ['user','category','price','title','date_now']
    list_filter =['type','category']

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['title','slug']

class PlayerAdmin(admin.ModelAdmin):
    list_display = ['title','real_name','price']

    
# Register your models here.
admin.site.register(Product,ProductAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(Type)
admin.site.register(Player,PlayerAdmin)
admin.site.register(Shoping,SepetAdmin)
admin.site.register(Payment, PaymentAdmin)
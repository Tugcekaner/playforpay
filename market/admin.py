from django.contrib import admin
from.models import *

class SepetAdmin(admin.ModelAdmin):
    list_display = ['user','product','piece','price','paymentCheck']
    list_filter = ['user','product','paymentCheck']

class PaymentAdmin(admin.ModelAdmin):
    list_display = ['user', 'total', 'paymentDate','paymentCheck']

    
# Register your models here.
admin.site.register(Product)
admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Player)
admin.site.register(Shoping,SepetAdmin)
admin.site.register(Payment, PaymentAdmin)
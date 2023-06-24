from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserInfo(models.Model):
   user = models.ForeignKey(User, verbose_name=("Kulanıcı"), on_delete=models.CASCADE)
   password = models.CharField(("Şifre"), max_length=50,null=True)
   
   def __str__(self):  
      return self.user.username

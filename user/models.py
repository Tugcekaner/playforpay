from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class UserInfo(models.Model):
   user = models.ForeignKey(User, verbose_name=("Kulanıcı"), on_delete=models.CASCADE)
   
   def __str__(self):  # admin panelndeki isimlendirmeyi değiştirir
      return self.user.username

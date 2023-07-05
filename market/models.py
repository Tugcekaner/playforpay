from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

# * oyunlar
class Category(models.Model):
    title = models.CharField(("Kategori"), max_length=50)
    slug = models.SlugField(("Slug"), blank=True)
    img = models.FileField(("Oyun Resmi"), upload_to='static', max_length=100,null=True)
    video_embed = models.TextField(("Video Embed Kodu"), null=True, blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# * satılan ürün tipi
class Type(models.Model):
    title = models.CharField(("Kategori"), max_length=50)
    slug = models.SlugField(("Slug"), blank=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

# * ürün
class Product(models.Model):
    user = models.ForeignKey(User, verbose_name=(
        "Kullanıcı - Satıcı"), on_delete=models.CASCADE)
    category = models.ForeignKey(Category, verbose_name=(
        "Kategori"), on_delete=models.CASCADE,null=True)
    type = models.ForeignKey(Type, verbose_name=(
        "Tür"), on_delete=models.CASCADE,null=True)
    title = models.CharField(("Ürün adı"), max_length=50)
    text = models.TextField(("İçerik"))
    image = models.FileField(
        ("Ürün Resmi"), upload_to='product', max_length=100)
    date_now = models.DateField(("Tarih"), auto_now_add=True)
    stok = models.IntegerField(("Stok"))
    price = models.FloatField(("Fiyat"), blank=True, null=True)

    def __str__(self):  # admin panelndeki isimlendirmeyi değiştirir
        return self.title

# * oyuncu
class Player(models.Model):
    user = models.ForeignKey(User, verbose_name=(
        "Kullanıcı - Satıcı"), on_delete=models.CASCADE)
    real_name = models.CharField(("Gerçek Adı:"), max_length=100,null=True)
    title = models.CharField(("Oyuncu Adı"), max_length=100)
    text = models.TextField(("İçerik"))
    image = models.FileField(
        ("Oyuncu Resmi"), upload_to='product', max_length=100)
    price = models.FloatField(("Fiyat"), blank=True, null=True)
    video_embed = models.TextField(("Video Embed Kodu"), null=True, blank=True)
    stok = models.IntegerField(("Stok"),null=True,blank=True, default=2)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):  # admin panelndeki isimlendirmeyi değiştirir
        return self.title
    
# * sepet
class Shoping(models.Model):
   user = models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
   product = models.ForeignKey(Product, verbose_name=("Ürün"), on_delete=models.CASCADE)
   piece = models.IntegerField(("Ürün adeti"))
   price = models.FloatField(("Ürün Sepet Fiyatı"), default=0)

   def save(self, *args,**kwargs):
      self.price = int(self.piece) * float(self.product.price)
      self.price = round(self.price,2)
      super().save(*args, **kwargs)

   def __str__(self):  # admin panelndeki isimlendirmeyi değiştirir
      return self.user.username


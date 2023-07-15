# Generated by Django 4.2.1 on 2023-07-15 06:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0017_payment_paymentcheck'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name': 'Oyun Adı', 'verbose_name_plural': 'Oyun Kategorileri'},
        ),
        migrations.AlterModelOptions(
            name='payment',
            options={'verbose_name': 'Ödeme', 'verbose_name_plural': 'Ödemeler'},
        ),
        migrations.AlterModelOptions(
            name='player',
            options={'verbose_name': 'Oyuncu', 'verbose_name_plural': 'Oyuncular'},
        ),
        migrations.AlterModelOptions(
            name='shoping',
            options={'verbose_name': 'Sepet', 'verbose_name_plural': 'Alışveriş Sepetleri'},
        ),
        migrations.AlterModelOptions(
            name='type',
            options={'verbose_name': 'Ürün Türü', 'verbose_name_plural': 'Ürün Türleri'},
        ),
    ]

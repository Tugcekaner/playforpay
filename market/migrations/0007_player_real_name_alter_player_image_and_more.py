# Generated by Django 4.2.1 on 2023-06-26 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0006_player'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='real_name',
            field=models.CharField(max_length=100, null=True, verbose_name='Gerçek Adı:'),
        ),
        migrations.AlterField(
            model_name='player',
            name='image',
            field=models.FileField(upload_to='product', verbose_name='Oyuncu Resmi'),
        ),
        migrations.AlterField(
            model_name='player',
            name='title',
            field=models.CharField(max_length=100, verbose_name='Oyuncu Adı'),
        ),
    ]

# Generated by Django 4.2.1 on 2023-06-22 15:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userinfo',
            name='img',
            field=models.ImageField(default='profile/default-profile.png', upload_to='profile', verbose_name='Profil Resmi'),
        ),
        migrations.AddField(
            model_name='userinfo',
            name='password',
            field=models.CharField(max_length=50, null=True, verbose_name='Şifre'),
        ),
    ]

# Generated by Django 4.2.1 on 2023-06-26 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('market', '0007_player_real_name_alter_player_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='video_link',
            field=models.URLField(blank=True, null=True, verbose_name='Video Linki'),
        ),
    ]

# Generated by Django 5.1.3 on 2024-12-04 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0003_restaurantdish_price"),
    ]

    operations = [
        migrations.AddField(
            model_name="restaurantgroup",
            name="title",
            field=models.CharField(default=0, max_length=64, verbose_name="Название"),
            preserve_default=False,
        ),
    ]

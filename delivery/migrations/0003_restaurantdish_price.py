# Generated by Django 5.1.3 on 2024-12-04 14:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0002_rename_tickets_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='restaurantdish',
            name='price',
            field=models.IntegerField(default=0, verbose_name='Цена'),
            preserve_default=False,
        ),
    ]

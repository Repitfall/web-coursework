# Generated by Django 5.1.3 on 2025-01-19 09:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0008_alter_historicalrestaurant_info_and_more"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="restaurant",
            options={"ordering": ["title"]},
        ),
        migrations.AddField(
            model_name="courier",
            name="type",
            field=models.CharField(
                choices=[("F", "Foot"), ("B", "Bicycle"), ("C", "Car")],
                default="F",
                max_length=1,
            ),
        ),
        migrations.AddField(
            model_name="historicalcourier",
            name="type",
            field=models.CharField(
                choices=[("F", "Foot"), ("B", "Bicycle"), ("C", "Car")],
                default="F",
                max_length=1,
            ),
        ),
    ]

# Generated by Django 5.1.3 on 2025-01-21 10:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0008_alter_courier_resume_alter_courier_url_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="historicalrestaurant",
            name="slug",
            field=models.SlugField(
                default="None", max_length=64, verbose_name="Ссылка"
            ),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name="restaurant",
            name="slug",
            field=models.SlugField(
                default="None", max_length=64, verbose_name="Ссылка"
            ),
            preserve_default=False,
        ),
    ]

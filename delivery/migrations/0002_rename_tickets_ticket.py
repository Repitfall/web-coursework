# Generated by Django 5.1.3 on 2024-12-04 10:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("delivery", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Tickets",
            new_name="Ticket",
        ),
    ]

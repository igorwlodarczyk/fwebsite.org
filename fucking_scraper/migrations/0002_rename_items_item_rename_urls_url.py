# Generated by Django 4.2.1 on 2023-05-04 16:00

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("fucking_scraper", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Items",
            new_name="Item",
        ),
        migrations.RenameModel(
            old_name="Urls",
            new_name="Url",
        ),
    ]

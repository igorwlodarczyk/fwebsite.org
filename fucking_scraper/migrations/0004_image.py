# Generated by Django 4.2.1 on 2023-05-05 18:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("fucking_scraper", "0003_item_slug"),
    ]

    operations = [
        migrations.CreateModel(
            name="Image",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "image_file",
                    models.ImageField(upload_to="fucking_scraper/files/item_photos"),
                ),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fucking_scraper.item",
                    ),
                ),
            ],
        ),
    ]

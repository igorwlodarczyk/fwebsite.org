# Generated by Django 4.2.1 on 2023-05-06 15:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("fucking_scraper", "0004_image"),
    ]

    operations = [
        migrations.CreateModel(
            name="LowestPrice",
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
                ("price", models.FloatField()),
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
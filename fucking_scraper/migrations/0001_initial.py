# Generated by Django 4.2.1 on 2023-05-04 15:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Items",
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
                ("brand", models.CharField(max_length=40)),
                ("model", models.CharField(max_length=160)),
            ],
        ),
        migrations.CreateModel(
            name="Urls",
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
                ("url", models.CharField(max_length=500)),
                ("store_name", models.CharField(max_length=150)),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fucking_scraper.items",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ScrapedData",
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
                ("currency", models.CharField(max_length=30)),
                ("size", models.CharField(max_length=30)),
                ("date", models.DateTimeField()),
                (
                    "item",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fucking_scraper.items",
                    ),
                ),
                (
                    "url",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="fucking_scraper.urls",
                    ),
                ),
            ],
        ),
    ]

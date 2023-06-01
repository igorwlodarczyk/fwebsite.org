from django.db import models
from django.utils.text import slugify

# Create your models here.


class Item(models.Model):
    brand = models.CharField(max_length=40)
    model = models.CharField(max_length=160)
    slug = models.SlugField(
        default="", null=False, blank=True, editable=False, db_index=True
    )

    def save(self, *args, **kwargs):
        self.slug = slugify(f"{self.brand} {self.model}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model}"


class Url(models.Model):
    url = models.CharField(max_length=500)
    store_name = models.CharField(max_length=150)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item} - {self.store_name}: {self.url}"


class ScrapedData(models.Model):
    price = models.FloatField()
    currency = models.CharField(max_length=30)
    size = models.CharField(max_length=30)
    date = models.DateTimeField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    url = models.ForeignKey(Url, on_delete=models.CASCADE)

    def __str__(self):
        return (
            f"{self.item} - f{self.price} - {self.currency} - {self.date} - {self.size}"
        )


class Image(models.Model):
    image_file = models.ImageField(upload_to="fucking_scraper/files/item_photos")
    item = models.ForeignKey(Item, on_delete=models.CASCADE)


class LowestPrice(models.Model):
    price = models.FloatField()
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.price} USD - {self.item} - {self.date}"


class PLN(models.Model):
    pln_rate = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.pln_rate} PLN for 1 USD - {self.date}"


class EUR(models.Model):
    eur_rate = models.FloatField()
    date = models.DateTimeField()

    def __str__(self):
        return f"{self.eur_rate} EUR for 1 USD - {self.date}"

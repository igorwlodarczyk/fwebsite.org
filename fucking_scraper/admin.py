from django.contrib import admin
from .models import Url, ScrapedData, Item, Image, LowestPrice, EUR, PLN

# Register your models here.


class ImageAdmin(admin.ModelAdmin):
    readonly_fields = ("id",)


admin.site.register(Url)
admin.site.register(Item)
admin.site.register(ScrapedData)
admin.site.register(Image, ImageAdmin)
admin.site.register(LowestPrice)
admin.site.register(EUR)
admin.site.register(PLN)

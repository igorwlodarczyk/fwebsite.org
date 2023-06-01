from django.urls import path

from . import views

urlpatterns = [
    path("", views.index),
    path("items/<slug:slug>/", views.item_detail, name="item_detail"),
    path("all-items", views.all_items, name="all_items"),
    path("about", views.about_page, name="about"),
]

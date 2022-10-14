from django.urls import path

from . import views

urlpatterns = [
    # Leave as empty string for base url
    path("", views.home, name="home"),
    path("mobiles", views.mobile_store, name="mobile"),
    path("laptops", views.laptop_store, name="laptop"),
    path("mobiles/<int:product_id>", views.mobile_score, name="mobile_score"),
    path("laptops/<int:product_id>", views.laptop_score, name="laptop_score"),
    # # path("<int:product_id>", views.score, name="score"),
]

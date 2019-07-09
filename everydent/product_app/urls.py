from django.urls import path

from product_app import views



urlpatterns = [
    path('manufacturers/', views.manufacturer_list, name="manufacturer_list"),
    path('manufacturers/<int:pk>/', views.manufacturer_detail, name="manufacturer_detial")
]

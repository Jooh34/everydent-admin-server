from django.urls import path

from product_app import views



urlpatterns = [
    path('count/', views.count_info, name="count_info"),
    path('expiry_list/', views.expiry_list, name="expiry_list"),
    path('manufacturers/', views.manufacturer_list, name="manufacturer_list"),
    path('manufacturers/<int:pk>/', views.manufacturer_detail, name="manufacturer_detial"),
    path('product_infos/', views.product_info_list, name="product_info_list"),
    path('product_infos/<int:pk>/', views.product_info_detail, name="product_info_detail"),
    path('products/', views.product_list, name="product_list"),
    path('products/<int:pk>/', views.product_detail, name="product_detial"),
    path('stock_list/<int:product_info_id>/', views.stock_list, name="stock_list"),
]

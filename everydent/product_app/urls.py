from django.urls import path

from product_app import views



urlpatterns = [
    path('count/', views.count_info, name="count_info"),
    path('expiry_list/', views.expiry_list, name="expiry_list"),
    path('running_out_list/', views.running_out_list, name="running_out_list"),

    path('manufacturers/', views.manufacturer_list, name="manufacturer_list"),
    path('manufacturers/<int:pk>/', views.manufacturer_detail, name="manufacturer_detial"),

    path('product_infos/', views.product_info_list, name="product_info_list"),
    path('product_infos/<int:pk>/', views.product_info_detail, name="product_info_detail"),
    path('product_infos/all/', views.product_info_all_list, name="product_info_all_detail"),
    path('product_infos/min_stock/', views.product_min_stock),

    path('products/', views.product_list, name="product_list"),
    path('products/<int:pk>/', views.product_detail, name="product_detial"),
    path('products/status/', views.product_status_list),
    path('products/status/<int:pk>/', views.product_status_detail),

    path('stock_list/<int:product_info_id>/', views.stock_list, name="stock_list"),
]

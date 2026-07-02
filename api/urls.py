from django.urls import path
from . import views

urlpatterns = [
    path("products/", views.ProductListCreateAPIView.as_view(), name="product_list"),
    # path("products/create/", views.ProductCreateAPIView.as_view(), name="product_create"),
    path("products/info/", views.ProductsInfoAPIView.as_view(), name="products_info"),
    path("products/<int:product_id>/", views.ProductDetailAPIView.as_view(), name="product_detail"),
    path("orders/", views.OrderListAPIView.as_view(), name="order_list"),
    path("user-orders/", views.UserOrderListAPIView.as_view(), name="user_order_list"),



]

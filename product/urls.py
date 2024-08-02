from django.urls import path

from .views import *

app_name="product"

urlpatterns = [
    path('api/product', ProductView.as_view(), name='product'),
    path('api/products', ProductsView.as_view(), name='products')
]

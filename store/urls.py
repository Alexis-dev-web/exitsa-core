from django.urls import path

from .views import *

app_name="store"

urlpatterns = [
    path('api/store', StoreView.as_view(), name='store'),
    path('api/stores', StoresView.as_view(), name='stores'),
    path('api/store/product', StoreProductView.as_view(), name='store_product')
]
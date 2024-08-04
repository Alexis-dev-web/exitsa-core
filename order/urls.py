from django.urls import path

from .views import *

app_name="order"

urlpatterns = [
    path('api/order', OrderView.as_view(), name='order'),
    path('api/orders', OrdersView.as_view(), name='orders'),
    path('api/order/report', ReportView.as_view(), name='report')
]

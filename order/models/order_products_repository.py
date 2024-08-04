from datetime import date
from django.db.models import Sum

from .order_products import OrderProduct


class OrderProductsRepository:

    def get_more_sale(self, start_date: date, end_date: date) -> OrderProduct:
        statuses = ['DELIVERED', 'SENT'] 
        return OrderProduct.objects.filter(order__status__in=statuses)\
            .filter(order__created_at__range=(start_date, end_date))\
                .values('product__name').annotate(total_sold=Sum('quantity'), total_price=Sum('price')).order_by('-total_sold')[:5]

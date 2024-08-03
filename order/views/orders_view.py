import logging
from rest_framework import status as api_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

from user.middlewares import permission_required

from order.dto import GetOrdersDTO
from order.use_case import GetOrdersUseCase
from order.serializers import GetOrdersSerializer


class OrdersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.get_orders_use_case = GetOrdersUseCase()

    @permission_required('view_order')
    def get(self, request, *args, **kwargs):
        self.logger.info(f"OrdersView#get START - Get orders - orderAgent={request.META.get('HTTP_order_AGENT', None)}")

        try:
            serializer = GetOrdersSerializer(data=request.GET)
            serializer.is_valid(raise_exception=True)
            
            orders = self.get_orders_use_case.execute(GetOrdersDTO.from_json(serializer.data))

            self.logger.info(f"OrdersView#post SUCCESS - Get orders - orderId={len(orders)}")

            return Response(orders, status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'OrdersView#get FAILURE - error to get orders - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'OrdersView#get FAILURE - error to get orders - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

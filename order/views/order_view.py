import logging
from rest_framework import status as api_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

from order.dto import CreateOrderDTO, UpdateOrderStateDTO
from order.use_case import CreateOrderUseCase, GetOrderUseCase, UpdateOrderStateUseCase, UpdateOrderUseCase
from order.serializers import OrderSerializer, GetOrderSerializer, UpdateOrderStateSerializer, UpdateOrderSerializer
from order.response import OrderResponse


class OrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.create_order_use_case = CreateOrderUseCase()
        self.get_order_use_case = GetOrderUseCase()
        self.update_order_state_use_case = UpdateOrderStateUseCase()
        self.order_response = OrderResponse()
        self.update_order_use_case = UpdateOrderUseCase()

    def post(self, request):
        self.logger.info(f"OrderView#post START - Create order - orderAgent={request.META.get('HTTP_order_AGENT', None)}")

        try:
            serializer = OrderSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            order = self.create_order_use_case.execute(CreateOrderDTO.from_json(serializer.data))

            self.logger.info(f"OrderView#post SUCCESS - Created order - orderId={order['id']}")

            return Response(order, status=api_status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            self.logger.error(f'OrderView#post FAILURE - error to create order - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'OrderView#post FAILURE - error to create order - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        self.logger.info(f"OrderView#get START - Get order - orderAgent={request.META.get('HTTP_order_AGENT', None)}")

        try:
            serializer = GetOrderSerializer(data=request.GET)
            serializer.is_valid(raise_exception=True)

            order = serializer.data['order']

            order = self.get_order_use_case.execute(order)
 
            self.logger.info(f"OrderView#post SUCCESS - Get order - orderId={order['id']}")

            return Response(order, status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'OrderView#get FAILURE - error to get order - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'OrderView#get FAILURE - error to get order - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def put(self, request):
        self.logger.info(f"OrderView#put START - Update order status- orderAgent={request.META.get('HTTP_order_AGENT', None)}")

        try:
            serializer = UpdateOrderStateSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            order = self.update_order_state_use_case.execute(UpdateOrderStateDTO.from_json(serializer.data))

            self.logger.info(f"OrderView#put SUCCESS - Updated order status - orderId={order.id}")

            return Response(self.order_response.to_json(order), status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'OrderView#put FAILURE - error to update order status - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'OrderView#put FAILURE - error to update order status - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        self.logger.info(f"OrderView#patch START - Update order - orderAgent={request.META.get('HTTP_order_AGENT', None)}")

        try:
            serializer = UpdateOrderSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            order = self.update_order_use_case.execute(CreateOrderDTO.from_json(serializer.data))

            self.logger.info(f"OrderView#patch SUCCESS - Updated order - orderId={order['id']}")

            return Response(order, status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'OrderView#patch FAILURE - error to update order - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'OrderView#patch FAILURE - error to update order - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)


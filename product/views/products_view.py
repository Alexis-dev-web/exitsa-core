import logging
from rest_framework import status as api_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

from product.dto import GetProductsDTO
from product.serializers import GetProductsSerializer
from product.use_case import GetProductsUseCase
from product.responses import ProductResponse


class ProductsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.product_response = ProductResponse()
        self.get_products_use_case = GetProductsUseCase()

    def get(self, request):
        self.logger.info(f"ProductsView#get START - Get products - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = GetProductsSerializer(data=request.GET)
            serializer.is_valid(raise_exception=True)

            products = self.get_products_use_case.execute(GetProductsDTO.from_json(serializer.validated_data))

            self.logger.info(f"ProductsView#get SUCCESS - Get products - products={len(products)}")

            return Response(products, status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'ProductsView#get FAILURE - error to get products - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'ProductsView#get FAILURE - error to get products - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

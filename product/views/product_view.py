import logging
from rest_framework import status as api_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

from user.middlewares import permission_required

from product.dto import CreateOrUpdateDTO
from product.serializers import GetProductSerializer, CreateProductSerializer, UpdateProductSerializer
from product.use_case import CreateOrUpdateProductUseCase, DeleteProductUseCase
from product.responses import ProductResponse


class ProductView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.product_response = ProductResponse()
        self.create_product_use_case = CreateOrUpdateProductUseCase()
        self.delete_product_use_case = DeleteProductUseCase()

    @permission_required('view_product')
    def get(self, request):
        self.logger.info(f"ProductView#get START - Get product - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = GetProductSerializer(data=request.GET)
            serializer.is_valid(raise_exception=True)

            product = serializer.data['product']

            self.logger.info(f"ProductView#post SUCCESS - Get product - productId={product.id}")

            return Response(self.product_response.to_json(product), status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'ProductView#get FAILURE - error to get product - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'ProductView#get FAILURE - error to get product - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

    @permission_required('add_product')
    def post(self, request):
        self.logger.info(f"ProductView#post START - Create product - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = CreateProductSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            product = self.create_product_use_case.execute(CreateOrUpdateDTO.from_json(serializer.data))

            self.logger.info(f"ProductView#post SUCCESS - Created store - productId={product.id}")

            return Response(self.product_response.to_json(product), status=api_status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            self.logger.error(f'ProductView#post FAILURE - error to create product - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'ProductView#post FAILURE - error to create product - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

    @permission_required('change_product')
    def patch(self, request):
        self.logger.info(f"ProductView#patch START - Update product - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = UpdateProductSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            product = self.create_product_use_case.execute(CreateOrUpdateDTO.from_json(serializer.data))

            self.logger.info(f"ProductView#patch SUCCESS - Udated store - productId={product.id}")

            return Response(self.product_response.to_json(product), status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'ProductView#patch FAILURE - error to update product - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'ProductView#patch FAILURE - error to update product - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

    @permission_required('delete_product')
    def delete(self, request):
        self.logger.info(f"ProductView#delete START - Delete product - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = GetProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            product = serializer.data['product']
            self.delete_product_use_case.execute(product)
            self.logger.info(f"ProductView#delete SUCCESS - deleted product - productId={product.id}")

            return Response(status=api_status.HTTP_204_NO_CONTENT)
        except serializers.ValidationError as error:
            self.logger.error(f'ProductView#delete FAILURE - error to delete product - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'ProductView#delete FAILURE - error to delete product - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)
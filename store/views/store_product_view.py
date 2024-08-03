import logging
from rest_framework import status as api_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

from user.middlewares import permission_required

from store.serializers import AddProductToSoreSerializer
from store.dto import AddProductToStoreDTO
from store.use_case import AddProductToStoreUseCase
from store.response import StoreProductResponse


class StoreProductView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.add_product_to_store_use_case = AddProductToStoreUseCase()
        self.store_product_response = StoreProductResponse()

    @permission_required('add_storehasproduct')
    def post(self, request):
        self.logger.info(f"StoreProductView#post START - Add product to store - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = AddProductToSoreSerializer(data=request.data)
            
            serializer.is_valid(raise_exception=True)

            store_product = self.add_product_to_store_use_case.execute(AddProductToStoreDTO.from_json(serializer.data))

            self.logger.info(f"StoreProductView#post SUCCESS - Added product to store - storeProductId={store_product.id}")

            return Response(self.store_product_response.to_json(store_product), status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'StoreProductView#post FAILURE - error to add product to store - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'StoreProductView#post FAILURE - error to add product to s - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)


import logging
from rest_framework import status as api_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

from store.dto import CreateOrUpdateStoreDTO
from store.response import StoreResponse
from store.serializers import CreateStoreSerializer, GetStoreSerializer, UpdatetoreSerializer
from store.use_case import CreateOrUpdateStoreUseCase


class StoreView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.create_store_use_case = CreateOrUpdateStoreUseCase()
        self.store_response = StoreResponse()

    def get(self, request):
        self.logger.info(f"StoreView#get START - Get store - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = GetStoreSerializer(data=request.GET)
            serializer.is_valid(raise_exception=True)

            store = serializer.data['store']

            self.logger.info(f"StoreView#post SUCCESS - Get store - storeId={store.id}")

            return Response(self.store_response.to_json(store), status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'StoreView#get FAILURE - error to get store - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'StoreView#get FAILURE - error to get store - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        self.logger.info(f"StoreView#post START - Create store - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = CreateStoreSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            store = self.create_store_use_case.execute(CreateOrUpdateStoreDTO.from_json(serializer.data))

            self.logger.info(f"StoreView#post SUCCESS - Created store - storeId={store.id}")

            return Response(self.store_response.to_json(store), status=api_status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            self.logger.error(f'StoreView#post FAILURE - error to create store - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'StoreView#post FAILURE - error to create store - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        self.logger.info(f"StoreView#patch START - Update store - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = UpdatetoreSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            store = self.create_store_use_case.execute(CreateOrUpdateStoreDTO.from_json(serializer.data))

            self.logger.info(f"StoreView#patch SUCCESS - Updated store - storeId={store.id}")

            return Response(self.store_response.to_json(store), status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'StoreView#post FAILURE - error to update store - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'StoreView#post FAILURE - error to update store - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)


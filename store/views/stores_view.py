import logging
from rest_framework import status as api_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from user.middlewares import permission_required

from store.use_case import GetStoresUseCase


class StoresView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.get_stores_use_case = GetStoresUseCase()

    @permission_required('view_store')
    def get(self, request):
        self.logger.info(f"StoresView#get START - Get stores - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            stores = self.get_stores_use_case.execute()

            self.logger.info(f"StoresView#post SUCCESS - Get stores - stores={len(stores)}")

            return Response(stores, status=api_status.HTTP_200_OK)
        except Exception as error_message:
            self.logger.error(f'StoresView#get FAILURE - error to get stores - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)


import logging
from rest_framework import status as api_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

from user.dto import GetUsersDTO
from user.use_case import GetUsersUseCase
from user.response import UserResponse
from user.serializers import GetUsersSerializer


class UsersView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.get_users_use_case = GetUsersUseCase()
        self.user_response = UserResponse()

    def get(self, request):
        self.logger.info(f"UsersView#get START - Get users - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = GetUsersSerializer(data=request.GET)
            serializer.is_valid(raise_exception=True)

            users = self.get_users_use_case.execute(GetUsersDTO.from_json(serializer.data))

            self.logger.info(f"UsersView#get SUCCESS - Get users - users={len(users['items'])}")

            return Response(users, status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'UsersView#get FAILURE - error to get users - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'UsersView#get FAILURE - error to get users - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

import logging
from rest_framework import status as api_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action

from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

from user.dto import ChangePasswordDTO, CreateUserDTO
from user.use_case import ChangePasswordUseCase, CreateUserUseCase
from user.serializers import ChangePasswordSerializer, CreateUserSerializer
from user.response import UserResponse


class ProfileView(APIView):
    permission_classes = [AllowAny]

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.change_password_use_case = ChangePasswordUseCase()
        self.user_response = UserResponse()
        self.create_user_use_case = CreateUserUseCase()

    def patch(self, request):
        self.logger.info(f"ProfileView#patch START - Change password - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = ChangePasswordSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            user = self.change_password_use_case.execute(ChangePasswordDTO.from_json(serializer.data))

            self.logger.info(f"ProfileView#patch SUCCESS - Changed password - userId={user.id}")

            return Response(self.user_response.to_json(user), status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'ProfileView#patch FAILURE - error to change user - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'ProfileView#patch FAILURE - error to change user - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        self.logger.info(f"ProfileView#post START - Create user - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = CreateUserSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            user_dto = CreateUserDTO.from_json(serializer.data)
            user_dto.origin = 'FORM'
            
            user = self.create_user_use_case.execute(user_dto)

            self.logger.info(f"ProfileView#post SUCCESS - Create user - userId={user.id}")

            return Response(self.user_response.to_json(user), status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'ProfileView#post FAILURE - error to create use - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'ProfileView#post FAILURE - error to create use - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

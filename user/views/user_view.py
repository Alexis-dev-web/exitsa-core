import logging
from rest_framework import status as api_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

from user.dto import CreateUserDTO, UpdateUserDTO
from user.use_case import CreateUserUseCase, UpdateUserUseCase
from user.serializers import CreateUserSerializer, UpdateUserSerializer, GetUserSerializer
from user.response import UserResponse


class UserView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.create_user_use_case = CreateUserUseCase()
        self.user_response = UserResponse()
        self.update_user_use_case = UpdateUserUseCase()

    def get(self, request):
        self.logger.info(f"UserView#get START - Get user - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = GetUserSerializer(data=request.GET)
            serializer.is_valid(raise_exception=True)

            user = serializer.data['user']

            self.logger.info(f"UserView#post SUCCESS - Get user - userId={user.id}")

            return Response(self.user_response.to_json(user), status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'UserView#get FAILURE - error to get user - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'UserView#get FAILURE - error to get user - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        self.logger.info(f"UserView#post START - Create user - userAgent={request.META['HTTP_USER_AGENT']}")

        try:
            serializer = CreateUserSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            user = self.create_user_use_case.execute(CreateUserDTO.from_json(serializer.data))

            self.logger.info(f"UserView#post SUCCESS - Created user - userId={user.id}")

            return Response(self.user_response.to_json(user), status=api_status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            self.logger.error(f'UserView#post FAILURE - error to create user - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'UserView#post FAILURE - error to create user - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        self.logger.info(f"UserView#patch START - Update user - userAgent={request.META['HTTP_USER_AGENT']}")

        try:
            serializer = UpdateUserSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            user = self.update_user_use_case.execute(UpdateUserDTO.from_json(serializer.data))

            self.logger.info(f"UserView#patch SUCCESS - Update user - userId={user.id}")

            return Response(self.user_response.to_json(user), status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'UserView#patch FAILURE - error to update user - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'UserView#patch FAILURE - error to update user - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)
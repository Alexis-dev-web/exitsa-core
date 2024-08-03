import logging
from rest_framework import status as api_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

from user.dto import ChangePasswordDTO
from user.use_case import ChangePasswordUseCase
from user.serializers import ChangePasswordSerializer
from user.response import UserResponse
from user.middlewares import permission_required


class ProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.change_password_use_case = ChangePasswordUseCase()
        self.user_response = UserResponse()

    @permission_required('iam_change_password')
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

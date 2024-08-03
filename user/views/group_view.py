import logging
from rest_framework import status as api_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

from user.middlewares import permission_required

from user.dto import CreateGroupDTO
from user.use_case import CreateGroupUseCase
from user.serializers import CreateGroupSerializer, GetGroupSerializer
from user.response import GroupResponse


class GroupView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.create_group_use_case = CreateGroupUseCase()
        self.group_response = GroupResponse()

    @permission_required('view_group')
    def get(self, request):
        self.logger.info(f"GroupView#get START - Get group - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = GetGroupSerializer(data=request.GET)
            serializer.is_valid(raise_exception=True)

            group = serializer.data['group']

            self.logger.info(f"GroupView#post SUCCESS - Get group - userId={group.id}")

            return Response(self.group_response.get_group_with_permission(group), status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'GroupView#get FAILURE - error to get group - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'GroupView#get FAILURE - error to get group - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

    @permission_required('add_group')
    def post(self, request):
        self.logger.info(f"GroupView#post START - Create group - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = CreateGroupSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            group = self.create_group_use_case.execute(CreateGroupDTO.from_json(serializer.data))

            self.logger.info(f"GroupView#post SUCCESS - Created group - userId={group['id']}")

            return Response(group, status=api_status.HTTP_201_CREATED)
        except serializers.ValidationError as error:
            self.logger.error(f'GroupView#post FAILURE - error to create group - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'GroupView#post FAILURE - error to create group - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

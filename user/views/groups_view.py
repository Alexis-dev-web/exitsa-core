import logging
from rest_framework import status as api_status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers

from user.middlewares import permission_required

from user.dto import GetUsersDTO
from user.use_case import GetGroupsUseCase
from utils.serializers.base_paginate_serializer import BasePaginateSerializer 


class GroupsView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        self.get_groups_use_case = GetGroupsUseCase()

    @permission_required('view_group')
    def get(self, request):
        self.logger.info(f"GroupsView#get START - Get groups - userAgent={request.META.get('HTTP_USER_AGENT', None)}")

        try:
            serializer = BasePaginateSerializer(data=request.GET)
            serializer.is_valid(raise_exception=True)

            groups = self.get_groups_use_case.execute(GetUsersDTO.from_json(serializer.data))

            self.logger.info(f"GroupsView#get SUCCESS - Get users - groups={len(groups['items'])}")

            return Response(groups, status=api_status.HTTP_200_OK)
        except serializers.ValidationError as error:
            self.logger.error(f'GroupsView#get FAILURE - error to get groups - message{str(error.detail)})')
            return Response({"message": error.detail}, status=api_status.HTTP_400_BAD_REQUEST)
        except Exception as error_message:
            self.logger.error(f'GroupsView#get FAILURE - error to get groups - message{str(error_message)})')
            return Response({"message": str(error_message)}, status=api_status.HTTP_500_INTERNAL_SERVER_ERROR)

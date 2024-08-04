from unittest.mock import patch

from utils.tests.base_general_test import BaseGeneralTest
from utils.dto.paginate_base_dto import PaginateBaseDTO
from user.tests.dummy_date import UserDummyData

from user.use_case import GetGroupsUseCase


class GetGroupsUseCaseTest(BaseGeneralTest):

    def setUp(self):
        self.dummy_data = UserDummyData()
        self.get_groups_use_case = GetGroupsUseCase()

    @patch('django.contrib.auth.models.Group.objects.all')
    @patch('django.contrib.auth.models.Group.permissions')
    def test_create_user(self, mock_permissions, mock_repostory):
        group = self.dummy_data.basic_group()
        group_two = self.dummy_data.basic_group()

        mock_repostory.return_value = [group, group_two]
        mock_permissions.all.return_value = []
        response = self.get_groups_use_case.execute(PaginateBaseDTO.from_json({}))

        self.assertEqual(2, len(response['items']))

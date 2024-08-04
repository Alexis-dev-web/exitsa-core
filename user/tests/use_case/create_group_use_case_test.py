from unittest.mock import patch

from utils.tests.base_general_test import BaseGeneralTest
from user.tests.dummy_date import UserDummyData
from user.dto import CreateGroupDTO
from user.use_case import CreateGroupUseCase


class CreateGroupUseCaseTest(BaseGeneralTest):

    def setUp(self):
        self.dummy_data = UserDummyData()
        self.create_group_use_case = CreateGroupUseCase()

    @patch('django.contrib.auth.models.Group')
    @patch('django.contrib.auth.models.Group.permissions')
    def test_create_user(self, mock_set, mock_group):
        request = self.dummy_data.dict_create_group()
        group = self.dummy_data.basic_group()

        mock_group = group
        mock_group.save = group
        mock_set.set = patch.object([1], 'set')

        response = self.create_group_use_case.execute(CreateGroupDTO.from_json(request))

        self.assertEqual(request['group'], response['name'])

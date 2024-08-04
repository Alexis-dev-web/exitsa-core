from unittest.mock import patch

from utils.tests.base_general_test import BaseGeneralTest
from user.tests.dummy_date import UserDummyData
from user.dto import CreateUserDTO
from user.use_case import CreateUserUseCase


class CreateUserUseCaseTest(BaseGeneralTest):

    def setUp(self):
        self.dummy_data = UserDummyData()
        self.create_user_use_case = CreateUserUseCase()

    @patch('user.models.User')
    @patch('user.models.GroupRepository')
    def test_create_user(self, mock_user_groups, mock_user):
        user = self.dummy_data.build_user_test()
        user_request = self.dummy_data.build_basic_request()
        group = self.dummy_data.basic_group()

        mock_user.save.return_value = user
        mock_user.groups.set = patch.object([group], 'set')
        mock_user.first.return_value = None
        mock_user_groups.get_by_name = group

        new_user = self.create_user_use_case.execute(CreateUserDTO.from_json(user_request))

        self.assertEqual(user_request['email'], new_user.email)

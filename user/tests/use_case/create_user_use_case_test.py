from unittest.mock import patch

from utils.tests.base_general_test import BaseGeneralTest
from user.tests.dummy_date import UserDummyData
from user.dto import CreateUserDTO
from user.use_case.create_user_use_case import CreateUserUseCase


class CreateUserUseCaseTest(BaseGeneralTest):

    def setUp(self):
        self.dummy_data = UserDummyData()
        self.create_user_use_case = CreateUserUseCase()

    @patch('user.models.User.save')
    def test_create_user(self, mock_user):
        user = self.dummy_data.build_user_test()
        user_request = self.dummy_data.build_basic_request()

        mock_user.return_value = user

        new_user = self.create_user_use_case.execute(CreateUserDTO.from_json(user_request))

        self.assertEqual(user_request['email'], new_user.email)

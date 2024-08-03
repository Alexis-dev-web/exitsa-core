from unittest.mock import patch

from utils.tests.base_general_test import BaseGeneralTest
from user.tests.dummy_date import UserDummyData
from user.dto import CreateUserDTO
from user.use_case import UpdateUserUseCase


class UpdateUserUseCaseTest(BaseGeneralTest):

    def setUp(self):
        self.dummy_data = UserDummyData()
        self.update_user_use_case = UpdateUserUseCase()

    @patch('user.models.User.save')
    def test_update_user(self, mock_user):
        user = self.dummy_data.build_user_test()
        user_request = self.dummy_data.build_basic_request()
        user_request['user'] = user
        user_request['user_id'] = str(user.id)

        mock_user.return_value = user

        new_user = self.update_user_use_case.execute(CreateUserDTO.from_json(user_request))

        self.assertEqual(user_request['email'], new_user.email)

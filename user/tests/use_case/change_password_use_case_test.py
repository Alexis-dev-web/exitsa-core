from unittest.mock import patch

from utils.tests.base_general_test import BaseGeneralTest
from user.tests.dummy_date import UserDummyData
from user.dto import ChangePasswordDTO
from user.use_case import ChangePasswordUseCase


class ChangePasswordUseCaseTest(BaseGeneralTest):

    def setUp(self):
        self.dummy_data = UserDummyData()
        self.change_password_use_case = ChangePasswordUseCase()

    @patch('user.models.User.save')
    def test_update_user(self, mock_user):
        user = self.dummy_data.build_user_test()
        user_request = {
            'user_id': str(user.id),
            'user': user,
            'password': 'newPassword',
            'confimr_password': 'newPassword',
        }

        mock_user.return_value = user

        new_user = self.change_password_use_case.execute(ChangePasswordDTO.from_json(user_request))

        self.assertEqual(user.email, new_user.email)

from unittest.mock import patch
from django.core.paginator import Paginator

from utils.tests.base_general_test import BaseGeneralTest
from user.tests.dummy_date import UserDummyData
from user.dto import GetUsersDTO
from user.use_case import GetUsersUseCase


class GetUsersUseCaseTest(BaseGeneralTest):

    def setUp(self):
        self.dummy_data = UserDummyData()
        self.get_users_use_case = GetUsersUseCase()

    @patch('user.models.UserRepository.get_all_paginate')
    def test_get_users_all(self, mock_user):
        user = self.dummy_data.build_user_test()
        user_two = self.dummy_data.build_user_test()
        users = [user, user_two]

        paginator = Paginator(users, 10)

        #mock
        mock_user.return_value = paginator

        get_user = {
            'page': 1
        }

        response = self.get_users_use_case.execute(GetUsersDTO.from_json(get_user))

        self.assertEqual(2, len(response['items']))

    @patch('user.models.UserRepository.get_by_email_paginate')
    def test_get_users_vy_email(self, mock_user):
        user = self.dummy_data.build_user_test()
        user_two = self.dummy_data.build_user_test()
        users = [user, user_two]

        paginator = Paginator(users, 10)

        #mock
        mock_user.return_value = paginator

        get_user = {
            'page': 1,
            'email': 'new'
        }

        response = self.get_users_use_case.execute(GetUsersDTO.from_json(get_user))

        self.assertEqual(2, len(response['items']))

    @patch('user.models.UserRepository.get_by_gender_paginate')
    def test_get_users_by_gender(self, mock_user):
        user = self.dummy_data.build_user_test()
        user_two = self.dummy_data.build_user_test()
        users = [user, user_two]

        paginator = Paginator(users, 10)

        #mock
        mock_user.return_value = paginator

        get_user = {
            'page': 1,
            'gender': 'M'
        }

        response = self.get_users_use_case.execute(GetUsersDTO.from_json(get_user))

        self.assertEqual(2, len(response['items']))
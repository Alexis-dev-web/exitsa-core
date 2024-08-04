
from django.core.paginator import Paginator

from unittest.mock import patch
from django.urls import reverse

from utils.base_test_case import BaseCase
from user.tests.dummy_date import UserDummyData


class UsersViewTest(BaseCase):

    def setUp(self):
        self.dummy_data = UserDummyData()
        return super().setUp()

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_users_invalid_page(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        request = self.dummy_data.request_args_get()
        request['page'] = 'pip'

        #mock
        mock_authenticate.return_value = (user_login, None)
        
        url = reverse("user:users")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data=request,
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'page': ['A valid integer is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_users_invalid_limit(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        request = self.dummy_data.request_args_get()
        request['limit'] = 'pip'

        #mock
        mock_authenticate.return_value = (user_login, None)
        
        url = reverse("user:users")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data=request,
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'limit': ['A valid integer is required.']})

       
    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_users_invalid_gender(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        request = self.dummy_data.request_args_get()
        request['gender'] = 'pip'

        #mock
        mock_authenticate.return_value = (user_login, None)
        
        url = reverse("user:users")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data=request,
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'gender': ['"pip" is not a valid choice.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('user.models.UserRepository.get_all_paginate')
    def test_succesful_get_all_users(self, mock_get_users, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        request = self.dummy_data.request_args_get()

        users = [user_login]

        paginator = Paginator(users, 10)
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_get_users.return_value = paginator
        
        url = reverse("user:users")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data=request,
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(data['items']))

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('user.models.UserRepository.get_by_email_paginate')
    def test_succesful_get_all_users_by_email(self, mock_get_users, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        request = self.dummy_data.request_args_get()
        request['email'] = 'new_email'

        users = [user_login]

        paginator = Paginator(users, 10)
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_get_users.return_value = paginator
        
        url = reverse("user:users")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data=request,
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(data['items']))

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('user.models.UserRepository.get_by_gender_paginate')
    def test_succesful_get_all_users_by_gender(self, mock_get_users, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        request = self.dummy_data.request_args_get()
        request['gender'] = 'M'

        users = [user_login]

        paginator = Paginator(users, 10)
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_get_users.return_value = paginator
        
        url = reverse("user:users")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data=request,
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(1, len(data['items']))

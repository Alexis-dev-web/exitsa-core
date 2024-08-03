import json

from unittest.mock import patch
from django.urls import reverse

from utils.base_test_case import BaseCase
from utils.error_messages import messages
from user.tests.dummy_date import UserDummyData


class ProfileViewTest(BaseCase):

    def setUp(self):
        self.dummy_data = UserDummyData()
        return super().setUp()

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_change_password_missing_password(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        request = self.dummy_data.request_change_password()
        request.pop('password', None)

        #mock
        mock_authenticate.return_value = (user_login, None)
        
        url = reverse("user:profile")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'password': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_change_password_missing_confirm_password(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        request = self.dummy_data.request_change_password()
        request.pop('confirm_password', None)

        #mock
        mock_authenticate.return_value = (user_login, None)
        
        url = reverse("user:profile")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'confirm_password': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_change_password_not_match(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        request = self.dummy_data.request_change_password()
        request['confirm_password'] = 'Other'

        #mock
        mock_authenticate.return_value = (user_login, None)
        
        url = reverse("user:profile")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'password': [messages['passwords_not_equal']]})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_change_user_id_required(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        request = self.dummy_data.request_change_password()
        request.pop('user_id', None)

        #mock
        mock_authenticate.return_value = (user_login, None)
        
        url = reverse("user:profile")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'user_id': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('user.models.UserRepository.get_by_id')
    def test_change_user_not_exist(self, mock_user, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        request = self.dummy_data.request_change_password()

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_user.return_value = None
        
        url = reverse("user:profile")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'user': [messages['user_not_exist']]})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('user.models.UserRepository.get_by_id')
    @patch('user.models.User.save')
    def test_change_password_successful(self, mock_save, mock_user, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        request = self.dummy_data.request_change_password(user_login.id)

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_user.return_value = user_login
        
        url = reverse("user:profile")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['first_name'], user_login.first_name)

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

    def test_save_user_first_name_required(self):
        json_request = self.dummy_data.build_basic_request()
        json_request.pop('first_name', None)

        url = reverse("user:profile")

        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'first_name': ['This field is required.']})

    def test_save_user_last_name_required(self):
        json_request = self.dummy_data.build_basic_request()
        json_request.pop('last_name', None)

        url = reverse("user:profile")

        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'last_name': ['This field is required.']})

    def test_save_user_email_required(self):
        json_request = self.dummy_data.build_basic_request()
        json_request.pop('email', None)

        url = reverse("user:profile")

        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'email': ['This field is required.']})

    def test_save_user_gender_required(self):
        json_request = self.dummy_data.build_basic_request()
        json_request.pop('gender', None)

        url = reverse("user:profile")

        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'gender': ['This field is required.']})

    def test_save_user_gender_invalid(self):
        json_request = self.dummy_data.build_basic_request()
        json_request['gender'] = 'P'

        url = reverse("user:profile")

        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'gender': ['"P" is not a valid choice.']})

    def test_save_user_missing_password(self):
        json_request = self.dummy_data.build_basic_request()
        json_request.pop('password', None)

        url = reverse("user:profile")

        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'password': ['This field is required.']})

    def test_save_user_missing_confirm_password(self):
        json_request = self.dummy_data.build_basic_request()
        json_request.pop('confirm_password', None)

        url = reverse("user:profile")

        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'confirm_password': ['This field is required.']})

    def test_save_user_invalid_email(self):
        json_request = self.dummy_data.build_basic_request()
        json_request['email'] = 'alwex'

        url = reverse("user:profile")

        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'email': ['Enter a valid email address.']})

    def test_save_user_invalid_birthday(self):
        json_request = self.dummy_data.build_basic_request()
        json_request['birthday'] = 'alwex'

        url = reverse("user:profile")

        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'birthday': ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.']})

    def test_save_user_phone_max_lenght(self):
        json_request = self.dummy_data.build_basic_request()
        json_request['phone'] = '5650451446465'

        url = reverse("user:profile")

        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'phone': ['Ensure this field has no more than 10 characters.']})

    def test_save_user_passwords_not_match(self):
        json_request = self.dummy_data.build_basic_request()
        json_request['confirm_password'] = '5650451446465'

        url = reverse("user:profile")

        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'password': ['The password and confirm password not match']})

    @patch('user.models.UserRepository.get_by_email')
    def test_save_user_email_already_exist(self, mock_user):
        user = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_basic_request()

        # mock
        mock_user.return_value = user
        url = reverse("user:profile")

        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'email': ['User already exist']})

    @patch('user.models.User')
    @patch('user.models.UserRepository')
    @patch('user.models.GroupRepository')
    def test_save_user_successful(self, mock_user_groups, mock_repository, mock_user):
        user = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_basic_request()
        group = self.dummy_data.basic_group()

        # mock
        mock_repository.get_by_email.return_value = None
        mock_user.save.return_value = user
        mock_user.first.return_value = None
        mock_user_groups.get_by_name = group

        url = reverse("user:profile")

        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['email'], json_request['email'])

import os
import django
import uuid

from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse

os.environ['DJANGO_SETTINGS_MODULE'] = 'exitosa_core.settings'
django.setup()

from rest_framework.test import APIClient

from user.models import User


class UserViewTest(TestCase):

    def setUp(self):
        self.client = APIClient()

    def build_user_test(self, email='testing@exitosa.test'):
        user = User()
        user.first_name = 'test'
        user.last_name = 'tets last name'
        user.email = email

        return user

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_user_user_id_required(self, mock_authenticate):
        user_login = self.build_user_test()
        #mock
        mock_authenticate.return_value = (user_login, None)
        
        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'user_id': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_user_invalid_user_id(self, mock_authenticate):
        user_login = self.build_user_test()
        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data={'user_id': '1234'},
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'user_id': ['Must be a valid UUID.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('user.models.user_repository.UserRepository.get_by_id')
    def test_get_user_user_not_exist(self, mock_user, mock_authenticate):
        user_login = self.build_user_test()
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_user.return_value = None

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data={'user_id': uuid.uuid4()},
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], ['User does not exist'])

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('user.models.user_repository.UserRepository.get_by_id')
    def test_successful_get_user(self, mock_user, mock_authenticate):
        user_login = self.build_user_test()
        user_test = self.build_user_test('testi3ng@exitosa.test')

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_user.return_value = user_test

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data={'user_id': uuid.uuid4()},
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['email'], 'testi3ng@exitosa.test')
import uuid
import json

from unittest.mock import patch
from django.urls import reverse

from utils.base_test_case import BaseCase
from utils.error_messages import messages
from user.tests.dummy_date import UserDummyData



class UserViewTest(BaseCase):

    def setUp(self):
        self.dummy_data = UserDummyData()
        return super().setUp()

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_user_user_id_required(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
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
        user_login = self.dummy_data.build_user_test()
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
        user_login = self.dummy_data.build_user_test()
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
        self.assertEqual(data['message'], {'user': [messages['user_not_exist']]})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('user.models.user_repository.UserRepository.get_by_id')
    def test_successful_get_user(self, mock_user, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        user_test = self.dummy_data.build_user_test('testi3ng@exitosa.test')

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

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_save_user_first_name_required(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request.pop('first_name', None)

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'first_name': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_save_user_last_name_required(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request.pop('last_name', None)
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'last_name': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_save_user_email_required(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request.pop('email', None)

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'email': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_save_user_invalid_email(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request['email'] = 'myemail'

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'email': ['Enter a valid email address.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_save_user_password(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request.pop('password', None)

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'password': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_save_user_confirm_password(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request.pop('confirm_password', None)
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'confirm_password': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_save_user_gender_required(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request.pop('gender', None)
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'gender': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_save_user_gender_invalid(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request['gender'] = 'P'
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'gender': ['"P" is not a valid choice.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_save_user_birthday_invalid_format(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request['birthday'] = '01-02-2024'

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'birthday': ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_save_user_passwords_not_match(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request['confirm_password'] = 'other'

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'password': [messages['passwords_not_equal']]})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('user.models.UserRepository.get_by_email')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_save_user_user_already_exists(self, mock_group, mock_user_email, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        second_user = self.dummy_data.build_user_test('test2@exitosa.test')
    
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group
        mock_user_email.return_value = second_user

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'email': [messages['user_exist']]})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('user.models.UserRepository.get_by_email')
    @patch('user.models.User.save')
    @patch('user.models.GroupRepository.get_by_name')
    @patch('user.models.User.groups')
    def test_successful_save(self, mock_user_groups, mock_group, mock_save_user, mock_user_email, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_basic_request()
        second_user = self.dummy_data.build_user_test('test2@exitosa.test')
        group = self.dummy_data.basic_group()
        
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group
        mock_user_email.return_value = None
        mock_save_user.return_value = second_user
        mock_user_groups.set = patch.object([group], 'set')
        mock_user_groups.first.return_value = None

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['email'], json_request['email'])

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_update_user_first_name_required(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request['user_id'] = str(uuid.uuid4())
        json_request.pop('first_name', None)
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'first_name': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_update_user_last_name_required(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request['user_id'] = str(uuid.uuid4())
        json_request.pop('last_name', None)
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'last_name': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_update_user_email_required(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request['user_id'] = str(uuid.uuid4())
        json_request.pop('email', None)
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'email': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_update_user_invalid_email(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request['email'] = 'myemail'
        json_request['user_id'] = str(uuid.uuid4())

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'email': ['Enter a valid email address.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_update_user_gender_required(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request['user_id'] = str(uuid.uuid4())
        json_request.pop('gender', None)
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'gender': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_update_user_gender_invalid(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request['user_id'] = str(uuid.uuid4())
        json_request['gender'] = 'P'
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'gender': ['"P" is not a valid choice.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_update_user_birthday_invalid_format(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request['birthday'] = '01-02-2024'
        json_request['user_id'] = str(uuid.uuid4())

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'birthday': ['Date has wrong format. Use one of these formats instead: YYYY-MM-DD.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_update_user_id_required(self, mock_group, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'user_id': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('user.models.UserRepository.get_by_id')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_save_user_user_not_exists(self, mock_group, mock_user_get_by_id, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        json_request['user_id'] = str(uuid.uuid4())
    
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group
        mock_user_get_by_id.return_value = None

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'user': [messages['user_not_exist']]})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('user.models.UserRepository.get_by_id')
    @patch('user.models.UserRepository.get_by_email')
    @patch('django.contrib.auth.models.Group.objects.all')
    def test_update_user_user_not_exists(self, mock_group, mock_get_by_email, mock_user_get_by_id, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        group = self.dummy_data.basic_group()
        json_request = self.dummy_data.build_basic_request()
        second_user = self.dummy_data.build_user_test('test2@exitosa.test')
        json_request['user_id'] = str(second_user.id)

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group
        mock_user_get_by_id.return_value = second_user
        mock_get_by_email.return_value = user_login

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'user': [messages['user_exist']]})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('user.models.UserRepository.get_by_id')
    @patch('user.models.UserRepository.get_by_email')
    @patch('user.models.User.save')
    @patch('django.contrib.auth.models.Group.objects.all')
    @patch('user.models.User.groups')
    def test_successful_update(self, mock_user_groups, mock_group, mock_save_user, mock_get_by_email, mock_user_get_by_id, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_basic_request()
        second_user = self.dummy_data.build_user_test('test2@exitosa.test')
        json_request['user_id'] = str(second_user.id)
        group = self.dummy_data.basic_group()

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_group.return_value = group
        mock_user_get_by_id.return_value = second_user
        mock_get_by_email.return_value = second_user
        mock_save_user.return_value = second_user
        mock_user_groups.set = patch.object([group], 'set')
        mock_user_groups.first.return_value = None
        mock_user_groups.first.return_value = None

        url = reverse("user:user")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['first_name'], json_request['first_name'])

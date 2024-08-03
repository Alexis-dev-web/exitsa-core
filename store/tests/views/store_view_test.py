import uuid
import json

from unittest.mock import patch
from django.urls import reverse

from utils.base_test_case import BaseCase
from store.tests.dummy_data import StoreDummyData


class StoreViewTest(BaseCase):
    
    def setUp(self):
        self.dummy_data = StoreDummyData()
        return super().setUp()

    def create_store_dict(self):
        return {
            'name': 'New store',
            'description': 'New description',
            'type': 'DIGITAL',
            'url': 'http://127.0.0.1/testing'
        }

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_store_misisng_store_id(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'store_id': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_store_invalid_store_id(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data={'store_id': 'asassa'},
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'store_id': ['Must be a valid UUID.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('store.models.StoreRepository.get_by_id')
    def test_get_store_store_not_exist(self, mock_stores, mock_authenticate):
        user_login = self.dummy_data.build_user_test()

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_stores.return_value = None

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data={'store_id': uuid.uuid4()},
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'store': 'Store does not exist'})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('store.models.StoreRepository.get_by_id')
    def test_successful_get_store(self, mock_stores, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        store_test = self.dummy_data.build_store()

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_stores.return_value = store_test

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data={'store_id': uuid.uuid4()},
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], store_test.name)

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_create_store_missing_name(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.create_store_dict()
        json_request.pop('name', None)

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'name': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_create_store_missing_type(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.create_store_dict()
        json_request.pop('type', None)

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'type': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_create_store_invalid_type(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.create_store_dict()
        json_request['type'] = 'NONE'

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'type': ['"NONE" is not a valid choice.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('store.models.StoreRepository.get_by_name')
    def test_create_store_name_already_take(self, mock_store, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.create_store_dict()
        store = self.dummy_data.build_store()

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_store.return_value = store

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'store': ['Store already exist']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('store.models.StoreRepository.get_by_name')
    def test_create_store_name_invalid_url(self, mock_store, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.create_store_dict()
        json_request['url'] = 'no url'

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_store.return_value = None

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'url': ['Invalid url']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('store.models.StoreRepository.get_by_name')
    @patch('store.models.Store.save')
    def test_successful_create_store_name(self, mock_save_store, mock_store, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.create_store_dict()
        store = self.dummy_data.build_store()

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_store.return_value = None
        mock_save_store.return_value = store

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['name'], json_request['name'].upper())

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_store_missing_name(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.create_store_dict()
        json_request.pop('name', None)
        json_request['store_id'] = str(uuid.uuid4())

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'name': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_store_missing_type(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.create_store_dict()
        json_request.pop('type', None)
        json_request['store_id'] = str(uuid.uuid4())

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'type': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_store_invalid_type(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.create_store_dict()
        json_request['type'] = 'NONE'
        json_request['store_id'] = str(uuid.uuid4())

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'type': ['"NONE" is not a valid choice.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_store_missing_store_id(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.create_store_dict()

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'store_id': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('store.models.StoreRepository.get_by_id')
    def test_update_store_not_exists(self, mock_store_by_id, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.create_store_dict()
        json_request['store_id'] = str(uuid.uuid4())

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_store_by_id.return_value = None

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'store': 'Store does not exist'})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('store.models.StoreRepository.get_by_id')
    @patch('store.models.StoreRepository.get_by_name')
    def test_update_store_already_exists(self, mock_store_by_name, mock_store_by_id, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.create_store_dict()
        json_request['store_id'] = str(uuid.uuid4())
        store = self.dummy_data.build_store()
        store_two = self.dummy_data.build_store()
        store_two.name = 'Update store'

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_store_by_id.return_value = store
        mock_store_by_name.return_value = store_two

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'store': 'Store already exist'})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('store.models.StoreRepository.get_by_id')
    @patch('store.models.StoreRepository.get_by_name')
    def test_update_store_name_invalid_url(self, mock_store_by_name, mock_store_by_id, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.create_store_dict()
        json_request['url'] = 'no url'
        json_request['store_id'] = str(uuid.uuid4())
        store_two = self.dummy_data.build_store()
        store_two.name = 'Update store'

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_store_by_id.return_value = store_two
        mock_store_by_name.return_value = None

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'url': ['Invalid url']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('store.models.StoreRepository.get_by_id')
    @patch('store.models.StoreRepository.get_by_name')
    @patch('store.models.Store.save')
    def test_succcesful_update_store(self, mock_store_update, mock_store_by_name, mock_store_by_id, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.create_store_dict()
        json_request['store_id'] = str(uuid.uuid4())
        store_two = self.dummy_data.build_store()
        store_two.name = 'Update store'

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_store_by_id.return_value = store_two
        mock_store_by_name.return_value = None
        mock_store_update.return_value = store_two

        url = reverse("store:store")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], json_request['name'].upper())


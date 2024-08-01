import os
import django

from unittest.mock import patch
from django.urls import reverse

os.environ['DJANGO_SETTINGS_MODULE'] = 'exitosa_core.settings'
django.setup()

from utils.base_test_case import BaseCase
from store.tests.dummy_data import StoreDummyData


class StoresViewTest(BaseCase):
    
    def setUp(self):
        self.dummy_data = StoreDummyData()
        return super().setUp()

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('store.models.StoreRepository.get_all')
    def test_get_stores(self, mock_stores, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        store_test = self.dummy_data.build_store()
        store_test_2 = self.dummy_data.build_store()
        store_test_2.name = 'Second store'

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_stores.return_value = [store_test, store_test_2]

        url = reverse("store:stores")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data={'user_id': '1234'},
            content_type="application/json"
        )
        
        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), 2)

        
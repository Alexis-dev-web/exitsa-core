from unittest.mock import patch

from utils.tests.base_general_test import BaseGeneralTest
from store.tests.dummy_data import StoreDummyData
from store.dto import CreateOrUpdateStoreDTO
from store.use_case.create_store_use_case import CreateOrUpdateStoreUseCase


class CreateStoreUseCaseTest(BaseGeneralTest):

    def setUp(self):
        self.dummy_data = StoreDummyData()
        self.create_store_use_case = CreateOrUpdateStoreUseCase()

    def create_store_dict(self):
        return {
            'name': 'New store',
            'description': 'New description',
            'type': 'DIGITAL',
            'url': 'http://127.0.0.1/testing'
        }

    @patch('store.models.Store.save')
    def test_create_new_store(self, mock_store):
        store = self.dummy_data.build_store()

        store_request = CreateOrUpdateStoreDTO.from_json(self.create_store_dict())
        #mocks
        mock_store.return_value = store

        new_store = self.create_store_use_case.execute(store_request)

        self.assertEqual(new_store.name, store_request.name.upper())

    @patch('store.models.Store.save')
    def test_update_new_store(self, mock_store):
        store = self.dummy_data.build_store()

        store_request = CreateOrUpdateStoreDTO.from_json(self.create_store_dict())
        store_request.store_id = str(store.id)
        store_request.store = store

        #mocks
        mock_store.return_value = store

        new_store = self.create_store_use_case.execute(store_request)

        self.assertEqual(new_store.name, store_request.name.upper())

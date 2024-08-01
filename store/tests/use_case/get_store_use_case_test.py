from unittest.mock import patch

from utils.tests.base_general_test import BaseGeneralTest

from store.tests.dummy_data import StoreDummyData
from store.use_case import GetStoresUseCase


class GetStoresUseCaseTest(BaseGeneralTest):
    
    def setUp(self):
        self.dummy_data = StoreDummyData()
        self.get_stores_use_case = GetStoresUseCase()

    @patch('store.models.StoreRepository.get_all')
    def test_get_stores(self, mock_stores):
        store = self.dummy_data.build_store()

        #mock
        mock_stores.return_value = [store]

        stores = self.get_stores_use_case.execute()

        self.assertEqual(1, len(stores))

from unittest.mock import patch

from utils.tests.base_general_test import BaseGeneralTest

from product.tests.product_dummy import ProductDummy
from product.use_case import UpdateInventoryProductUseCase


class UpdateInventoryProductUseCaseTest(BaseGeneralTest):

    def setUp(self):
        self.dummy_data = ProductDummy()
        self.use_case = UpdateInventoryProductUseCase()

    @patch('product.models.Product.save')
    def test_update_inventory_buy_sent_product(self, mock_products):
        product = self.dummy_data.build_product_test()

        #mock 
        mock_products.return_value = product

        sent, date_sent = self.use_case.execute(product, 'BUY', 1, 'SENT')

        self.assertEqual(True, sent)

    @patch('product.models.Product.save')
    def test_update_inventory_sale_cancelled_product(self, mock_products):
        product = self.dummy_data.build_product_test()

        #mock 
        mock_products.return_value = product

        sent, date_sent = self.use_case.execute(product, 'SALE', 1, 'CANCELLED')

        self.assertEqual(False, sent)

    def test_update_inventory_sale_not_quantity_product(self):
        product = self.dummy_data.build_product_test()
        product.in_existence = 2

        sent, date_sent = self.use_case.execute(product, 'SALE', 3, 'SENT')

        self.assertEqual(False, sent)


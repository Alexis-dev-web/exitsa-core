from unittest.mock import patch

from utils.tests.base_general_test import BaseGeneralTest

from product.tests.product_dummy import ProductDummy
from product.use_case import DeleteProductUseCase


class DeleteProductUseCaseTest(BaseGeneralTest):

    def setUp(self):
        self.dummy_data = ProductDummy()
        self.use_case = DeleteProductUseCase()

    @patch('product.models.Product.save')
    def test_delete_product(self, mock_products):
        product = self.dummy_data.build_product_test()

        #mock 
        mock_products.return_value = product

        response = self.use_case.execute(product)

        self.assertEqual(False, response.is_active)

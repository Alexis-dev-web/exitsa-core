import uuid
from unittest.mock import patch

from utils.tests.base_general_test import BaseGeneralTest

from product.tests.product_dummy import ProductDummy
from product.dto import CreateOrUpdateDTO
from product.use_case import CreateOrUpdateProductUseCase


class CreateOrUpdateProductUseCaseTest(BaseGeneralTest):

    def setUp(self):
        self.dummy_data = ProductDummy()
        self.use_case = CreateOrUpdateProductUseCase()

    @patch('product.models.Product.save')
    def test_create_product(self, mock_products):
        product = self.dummy_data.build_product_test()
        request = self.dummy_data.build_dict_product()

        #mock 
        mock_products.return_value = product

        response = self.use_case.execute(CreateOrUpdateDTO.from_json(request))

        self.assertEqual(request['sku'], response.sku)

    @patch('product.models.Product.save')
    def test_update_product(self, mock_products):
        product = self.dummy_data.build_product_test()
        request = self.dummy_data.build_dict_product()
        request['product_id'] = uuid.uuid4()
        request['product'] = product
        
        #mock 
        mock_products.return_value = product

        response = self.use_case.execute(CreateOrUpdateDTO.from_json(request))

        self.assertEqual(request['sku'], response.sku)

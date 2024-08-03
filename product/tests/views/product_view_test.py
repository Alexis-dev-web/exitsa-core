import uuid
import json

from unittest.mock import patch
from django.urls import reverse

from utils.base_test_case import BaseCase
from product.tests.product_dummy import ProductDummy


class ProductViewTest(BaseCase):
    
    def setUp(self):
        self.dummy_data = ProductDummy()
        return super().setUp()

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_product_misisng_product_id(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'product_id': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_get_product_invalid_product_id(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data={'product_id': 'ssss'},
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'product_id': ['Must be a valid UUID.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('product.models.ProductRepository.get_by_id')
    def test_get_product_product_not_exist(self, mock_product, mock_authenticate):
        user_login = self.dummy_data.build_user_test()

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_product.return_value = None

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data={'product_id': uuid.uuid4()},
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'product': 'Product does not exist'})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('product.models.ProductRepository.get_by_id')
    def test_successful_get_product(self, mock_product, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        product = self.dummy_data.build_product_test()

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_product.return_value = product

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.get(
            url,
            data={'product_id': uuid.uuid4()},
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['name'], product.name)

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_create_product_missing_sku(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request.pop('sku', None)

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'sku': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_create_product_missing_name(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request.pop('name', None)

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

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
    def test_create_product_missing_description(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request.pop('description', None)

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'description': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_create_product_missing_type(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request.pop('type', None)

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

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
    def test_create_product_invalid_type(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['type'] = 'OTHER'

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'type': ['"OTHER" is not a valid choice.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_create_product_missing_state(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request.pop('state', None)

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'state': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_create_product_invalid_state(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['state'] = 'OTHER'

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'state': ['"OTHER" is not a valid choice.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_create_product_missing_base_pricing(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request.pop('base_pricing', None)

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'base_pricing': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_create_product_invalid_base_pricing(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['base_pricing'] = 'lol'
        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'base_pricing': ['A valid number is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_create_product_invalid_base_cost(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['base_cost'] = 'lol'
        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'base_cost': ['A valid number is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_create_product_invalid_in_existence(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['in_existence'] = 'lol'
        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'in_existence': ['A valid integer is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('product.models.ProductRepository.get_by_sku')
    def test_create_product_product_already_exist(self, mock_sku, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        product = self.dummy_data.build_product_test()

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_sku.return_value = product

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'sku': ['SKU already exist']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('product.models.ProductRepository.get_by_sku')
    @patch('product.models.Product.save')
    def test_successful_create_product(self, mock_save, mock_sku, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        product = self.dummy_data.build_product_test()

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_sku.return_value = None
        mock_save.return_value = product

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['sku'], json_request['sku'])

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_product_missing_sku(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['product_id'] = str(uuid.uuid4())
        json_request.pop('sku', None)

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'sku': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_product_missing_name(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['product_id'] = str(uuid.uuid4())
        json_request.pop('name', None)

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

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
    def test_update_product_missing_description(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['product_id'] = str(uuid.uuid4())
        json_request.pop('description', None)

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'description': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_product_missing_type(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['product_id'] = str(uuid.uuid4())
        json_request.pop('type', None)

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

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
    def test_update_product_invalid_type(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['product_id'] = str(uuid.uuid4())
        json_request['type'] = 'OTHER'

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'type': ['"OTHER" is not a valid choice.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_product_missing_state(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['product_id'] = str(uuid.uuid4())
        json_request.pop('state', None)

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'state': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_product_invalid_state(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['product_id'] = str(uuid.uuid4())
        json_request['state'] = 'OTHER'

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'state': ['"OTHER" is not a valid choice.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_product_missing_base_pricing(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['product_id'] = str(uuid.uuid4())
        json_request.pop('base_pricing', None)

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'base_pricing': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_product_invalid_base_pricing(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['product_id'] = str(uuid.uuid4())
        json_request['base_pricing'] = 'lol'
        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'base_pricing': ['A valid number is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_product_invalid_base_cost(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['product_id'] = str(uuid.uuid4())
        json_request['base_cost'] = 'lol'
        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'base_cost': ['A valid number is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_product_invalid_in_existence(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['product_id'] = str(uuid.uuid4())
        json_request['in_existence'] = 'lol'
        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'in_existence': ['A valid integer is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_product_missing_product_id(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'product_id': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_update_product_invalid_product_id(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        json_request['product_id'] = 'aksas'

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'product_id': ['Must be a valid UUID.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('product.models.ProductRepository.get_by_id')
    def test_update_product_product_not_exist(self, mock_by_id, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        product = self.dummy_data.build_product_test()
        json_request['product_id'] = str(uuid.uuid4())

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_by_id.return_value = None

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'product': 'Product does not exist'})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('product.models.ProductRepository.get_by_id')
    @patch('product.models.ProductRepository.get_by_sku')
    def test_update_product_product_already_exist(self, mocku_sku, mock_get_by_id, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        product = self.dummy_data.build_product_test()
        json_request['product_id'] = str(uuid.uuid4())

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_get_by_id.return_value = None
        mocku_sku.return_value = product

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.post(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'sku': ['SKU already exist']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('product.models.ProductRepository.get_by_sku')
    @patch('product.models.ProductRepository.get_by_id')
    @patch('product.models.Product.save')
    def test_successful_update_product(self, mock_save, mock_get_by_id, mock_sku, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = self.dummy_data.build_dict_product()
        product = self.dummy_data.build_product_test()
        json_request['product_id'] = str(uuid.uuid4())

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_sku.return_value = None
        mock_get_by_id.return_value = product
        mock_save.return_value = product

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.patch(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['sku'], json_request['sku'])


    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_delete_product_misisng_product_id(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()

        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.delete(
            url,
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'product_id': ['This field is required.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    def test_delete_product_invalid_product_id(self, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = {
            'product_id': 'assaas'
        }
        #mock
        mock_authenticate.return_value = (user_login, None)

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.delete(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'product_id': ['Must be a valid UUID.']})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('product.models.ProductRepository.get_by_id')
    def test_delete_product_product_not_exist(self, mock_product, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        json_request = {
            'product_id': str(uuid.uuid4())
        }
    
        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_product.return_value = None

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.delete(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        data = response.json()
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], {'product': 'Product does not exist'})

    @patch('rest_framework_simplejwt.authentication.JWTAuthentication.authenticate')
    @patch('product.models.ProductRepository.get_by_id')
    @patch('product.models.Product.save')
    def test_successful_delete_product(self, mock_save, mock_product, mock_authenticate):
        user_login = self.dummy_data.build_user_test()
        product = self.dummy_data.build_product_test()
        json_request = {
            'product_id': str(product.id)
        }

        #mock
        mock_authenticate.return_value = (user_login, None)
        mock_product.return_value = product
        mock_save.return_value = product

        url = reverse("product:product")

        self.client.credentials(HTTP_AUTHORIZATION='Bearer validtoken')
        response = self.client.delete(
            url,
            data=json.dumps(json_request),
            content_type="application/json"
        )

        self.assertEqual(response.status_code, 204)

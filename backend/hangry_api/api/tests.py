from django.test import TestCase
from rest_framework.test import APIClient


class FoodApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        response = self.client.post(
            '/api/category/',
            {'name': 'Handhelds', 'description': 'Sandwiches'},
            format='json',
        )
        self.category_id = response.data['data']['id']

    def test_food_can_be_created_with_category_id(self):
        response = self.client.post(
            '/api/food/',
            {
                'name': 'Test burger',
                'price': 5.25,
                'description': 'Test description',
                'category': self.category_id,
            },
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['data']['category'], 'Handhelds')

    def test_food_with_unknown_category_is_rejected(self):
        response = self.client.post(
            '/api/food/',
            {
                'name': 'Test burger',
                'price': 5.25,
                'description': 'Test description',
                'category': 999,
            },
            format='json',
        )

        self.assertEqual(response.status_code, 400)

    def test_missing_food_returns_not_found(self):
        response = self.client.get('/api/food/999')

        self.assertEqual(response.status_code, 404)


class OrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        category = self.client.post(
            '/api/category/',
            {'name': 'Handhelds', 'description': 'Sandwiches'},
            format='json',
        )
        food = self.client.post(
            '/api/food/',
            {
                'name': 'Test burger',
                'price': 5.25,
                'description': 'Test description',
                'category': category.data['data']['id'],
            },
            format='json',
        )
        self.food_id = food.data['data']['id']

    def test_order_rejects_non_positive_quantity(self):
        response = self.client.post(
            '/api/order/',
            {'name': 'test-order', 'item': self.food_id, 'quantity': 0},
            format='json',
        )

        self.assertEqual(response.status_code, 400)

    def test_order_rejects_unknown_food(self):
        response = self.client.post(
            '/api/order/',
            {'name': 'test-order', 'item': 999, 'quantity': 1},
            format='json',
        )

        self.assertEqual(response.status_code, 400)

    def test_order_returns_created_response(self):
        response = self.client.post(
            '/api/order/',
            {'name': 'test-order', 'item': self.food_id, 'quantity': 1},
            format='json',
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data['data']['item'], 'Test burger')

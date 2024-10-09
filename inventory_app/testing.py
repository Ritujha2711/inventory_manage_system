from django.test import TestCase
from rest_framework.test import APIClient
from .models import Item_details

class ItemTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.item = Item_details.objects.create(name='Test Item', description='Test description')

    def test_create_item(self):
        response = self.client.post('/api/items/', {'name': 'NewItem', 'description': 'New description'})
        self.assertEqual(response.status_code, 201)

    def test_get_item(self):
        response = self.client.get(f'/api/items/{self.item.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Test Item')

    def test_update_item(self):
        response = self.client.put(f'/api/items/{self.item.id}/', {'name': 'Updated', 'description': 'Updated desc'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'Updated')

    def test_delete_item(self):
        response = self.client.delete(f'/api/items/{self.item.id}/')
        self.assertEqual(response.status_code, 204)

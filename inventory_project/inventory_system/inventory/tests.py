# test_views.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Items

class ItemAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="testpass")
        self.token, _ = Token.objects.get_or_create(user=self.user)
        self.client.force_authenticate(user=self.user)
        self.item_data = {
            "name": "Test Item",
            "description": "Test Description"
        }
        self.create_url = reverse('create_item')  
        self.read_url = lambda id: reverse('read_item', kwargs={'id': id})  
        self.update_url = lambda id: reverse('read_item', kwargs={'id': id})  
        self.delete_url = lambda id: reverse('read_item', kwargs={'id': id})  

    def test_create_item_success(self):
        response = self.client.post(self.create_url, self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Item successfully created.")
        self.assertEqual(Items.objects.count(), 1)

    def test_create_item_duplicate(self):
        self.client.post(self.create_url, self.item_data, format='json')
        response = self.client.post(self.create_url, self.item_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['message'], "Item already exists.")

    def test_read_item_success(self):
        item = Items.objects.create(name="Read Item", description="Read Description")
        response = self.client.get(self.read_url(item.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['data']['name'], item.name)

    def test_read_item_not_found(self):
        response = self.client.get(self.read_url(999), format='json')  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "Item not found.")

    def test_update_item_success(self):
        item = Items.objects.create(name="Update Item", description="Update Description")
        update_data = {
            "name": "Updated Item",
            "description": "Updated Description"
        }
        response = self.client.put(self.update_url(item.id), update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Item successfully updated.")
        item.refresh_from_db()
        self.assertEqual(item.name, update_data['name'])

    def test_update_item_not_found(self):
        update_data = {
            "name": "Updated Item",
            "description": "Updated Description"
        }
        response = self.client.put(self.update_url(999), update_data, format='json')  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "Item not found.")

    def test_delete_item_success(self):
        item = Items.objects.create(name="Delete Item", description="Delete Description")
        response = self.client.delete(self.delete_url(item.id), format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Item successfully deleted")
        self.assertEqual(Items.objects.count(), 0)

    def test_delete_item_not_found(self):
        response = self.client.delete(self.delete_url(999), format='json')  
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['message'], "Item not found.")


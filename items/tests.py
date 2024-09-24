from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Item  # Adjust based on your actual model import

class ItemsAPITests(APITestCase):

    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(self.token))
        self.item = Item.objects.create(name='Test Item', description='Test Description')

    def test_create_item_success(self):
        url = reverse('item-list')  # This should match the URL pattern
        data = {'name': 'New Item', 'description': 'New Description'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_item_success(self):
        """Test retrieving an existing item."""
        url = reverse('item-detail', args=[self.item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_item_success(self):
        """Test updating an existing item."""
        url = reverse('item-detail', args=[self.item.id])
        data = {'name': 'Updated Item', 'description': 'Updated Description'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_item_success(self):
        """Test deleting an existing item."""
        url = reverse('item-detail', args=[self.item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    # Tests without authentication
    def test_create_item_unauthenticated(self):
        """Test creating an item without authentication."""
        self.client.credentials()  # Remove any authentication credentials
        url = reverse('item-list')
        data = {'name': 'Unauthorized Item', 'description': 'Unauthorized Description'}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_item_unauthenticated(self):
        """Test retrieving an item without authentication."""
        self.client.credentials()  # Remove any authentication credentials
        url = reverse('item-detail', args=[self.item.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_item_unauthenticated(self):
        """Test updating an item without authentication."""
        self.client.credentials()  # Remove any authentication credentials
        url = reverse('item-detail', args=[self.item.id])
        data = {'name': 'Unauthorized Update', 'description': 'Unauthorized Description'}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_delete_item_unauthenticated(self):
        """Test deleting an item without authentication."""
        self.client.credentials()  # Remove any authentication credentials
        url = reverse('item-detail', args=[self.item.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
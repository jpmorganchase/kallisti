from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase


class TestHealthAPI(APITestCase):
    def test_health_api(self):
        url = reverse('health')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {'status': 'up'})

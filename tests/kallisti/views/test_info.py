from django.urls import reverse
from django.test import override_settings
from rest_framework import status
from rest_framework.test import APITestCase


class TestInfoAPI(APITestCase):
    TEST_PLATFORM_INFO = {'test': 'test-platform-info'}

    @override_settings(KALLISTI_INFO_API_PLATFORM=TEST_PLATFORM_INFO)
    def test_info_api(self):
        url = reverse('info')

        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(["version", "platform"], list(response.data.keys()))
        self.assertEqual(self.TEST_PLATFORM_INFO, response.data["platform"])

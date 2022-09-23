# Django
from django.test import TestCase

# Python
import json
import os

# Django Rest Framework
from rest_framework.test import APIClient
from rest_framework import status


class UserTestCase(TestCase):

    def test_signup_user(self):
        """Check if we can create a user"""
        TestCase.skipTest()
        client = APIClient()
        response = client.post(
            '/users/signup/', {
                "email": "aldomm61@gmail.com",
                "password": "MiPass2022",
                "password_confirmation": "MiPass2022",
                "user_name": "Aldo",
                "user_last_name": "Matus",
                "state_id": 1
            },
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_user(self):
        client = APIClient()
        response = client.post(
            '/users/login', {
                'email': 'correodepruebaslinux@gmail.com',
                'password': 'Pass2022',
            },
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        result = json.loads(response.content)
        self.assertIn('access_token', result)


if __name__ == "__main__":
    os.environ["ALGORITHM"] = os.getenv('ALGORITHM')

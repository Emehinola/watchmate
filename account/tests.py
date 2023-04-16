from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

class RegisterTestCase(APITestCase):

    def test_registration(self):
        data: dict = {
            'username': 'bigsam',
            'email': 'bigsam@test.com',
            'password': 'Password@123',
            'password2': 'Password@123'
        }

        response = self.client.post(reverse('register'), data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)


class AuthenticationTestCase(APITestCase):

    # called before running test for creating temp. user
    def setUp(self):

        self.user = User.objects.create_user(username='bigsam', password='password')

    def test_login(self):
        data: dict = {
            'username': 'bigsam',
            'password': 'password'
        }

        response = self.client.post(reverse('login'), data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_logout(self):
        
        self.token = Token.objects.get(user__username='bigsam')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        response = self.client.post(reverse('logout'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
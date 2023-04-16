from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status

from . models import WatchList, StreamPlatform, Review
from .serializer import WatchListSerializer

class WatchlistTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='bigsam', password='password')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # add platform manually
        self.streamPlatform = StreamPlatform.objects.create(name='#1 Stream platformn worldwide', about='About this wonderful platform', website='https://platform.com')


    def test_platform_create(self): # for a non admin: returns forbidden
        data: dict = {
            'name': '#1 Stream platform',
            'about': 'Some goo times with this platform',
            'webiste': 'https://platform.com'
        }

        response = self.client.post(reverse('stream-platform'), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_platform_list(self):
        response = self.client.get(reverse('stream-platform'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_platform_ind(self):
        response = self.client.get(reverse('stream-details', args=(self.streamPlatform.id,)))

        self.assertEqual(response.status_code, status.HTTP_200_OK)

# testing for watchlist
class WatchlistTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='bigsam', password='password')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # add platform manually
        self.streamPlatform = StreamPlatform.objects.create(name='#1 Stream platformn worldwide', about='About this wonderful platform', website='https://platform.com')
        self.watchlist = WatchList.objects.create(platform=self.streamPlatform, title='A test title', active=True, description='A test desc')

    def test_watchlist_create(self):
        data = {
            'platform': self.streamPlatform,
            'title': 'A test title',
            'active': True,
            'descriptionn': 'A brief description',
        } 

        response = self.client.post(reverse('watchlist'), data=data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_watchlist_list(self):
        response = self.client.get(reverse('watchlist'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_watchlist_ind(self):
        response = self.client.get(reverse('movie_details', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

class ReviewTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='bigsam', password='password')
        self.token = Token.objects.get(user__username=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token.key)

        # add platform manually
        self.streamPlatform = StreamPlatform.objects.create(name='#1 Stream platformn worldwide', about='About this wonderful platform', website='https://platform.com')
        self.watchlist = WatchList.objects.create(platform=self.streamPlatform, title='A test title', active=True, description='A test desc')
        self.review = Review.objects.create(user=self.user, active=True, rating=3, watchlist=self.watchlist, description='A ashort description')

    def test_review_create(self):
        data = {
            'user': self.user,
            'active': True,
            'rating': 4.0,
            'watchlist': self.watchlist,
            'description': 'A short desc'
        }

        response = self.client.post(reverse('reviews-by-stream', args=(self.watchlist.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_review_update(self):
        data = {
            'user': self.user,
            'active': False,
            'rating': 3,
            'watchlist': self.watchlist,
            'description': 'A short desc -- updated'
        }

        response = self.client.put(reverse('review-detail', args=(self.review.id,)), data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_list(self):
        response = self.client.get(reverse('reviews-by-stream', args=(self.watchlist.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_ind(self):
        response = self.client.get(reverse('review-detail', args=(self.review.id,)))
        self.assertEqual(response.status_code, status.HTTP_200_OK)


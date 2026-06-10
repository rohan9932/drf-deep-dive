from django.test import TestCase
from . import models
from django.urls import reverse
from rest_framework import status

# Create your tests here.
# test for user-order/ endpoint
class UserOrderTestCase(TestCase):
    def setUp(self): # test user and orders 
        user1 = models.User.objects.create_user(username='user1', password='test')
        user2 = models.User.objects.create_user(username='user2', password='test')
        models.Order.objects.create(user=user1)
        models.Order.objects.create(user=user1)
        models.Order.objects.create(user=user2)
        models.Order.objects.create(user=user2)

    def test_user_order_endpoint_retrieves_only_authenticated_users_orders(self):
        user = models.User.objects.get(username='user2')
        # TestCase has a self.client attribute from which we can send requests to server
        self.client.force_login(user=user)
        # test sending reqeusts
        response = self.client.get(reverse('user_order_list'))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        orders = response.json() 
        # print(data)
        
        # testing if reponse order user is equal to user
        # all() -> returns true if all values in the object is true
        self.assertTrue(all(order['user'] == user.id for order in orders)) 

    def test_user_order_list_unauthenticated(self):
        response = self.client.get(reverse('user_order_list'))
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)  
from django.test import TestCase
from users.models import Users
from django.urls import reverse
# Create your tests here.


class UsersTestCase(TestCase):
    
    def setUp(self):
        Users.objects.create(username="test", password="test",
                             email="meemoo102039@gmail.com", phone="1234567890",
                             address="test", city="test", state="test",
                             country="test", zip="123456")
    
    def test_user_create(self):
        self.assertEqual(Users.objects.count(), 1)
        user = Users.objects.get(username="test")
        self.assertEqual(user.username, "test")
    
    def test_user_update(self):
        user = Users.objects.get(username="test")
        user.username = "test1"
        user.save()
        user = Users.objects.get(username="test1")
        self.assertNotEqual(user.username, None)
    
    def test_create_user_with_same_email(self):
        with self.assertRaises(Exception):
            Users.objects.create(username="test1", password="test1",
                                 email="meemoo102039@gmail.com", phone="1234567890",
                                 address="test", city="test", state="test",
                                 country="test", zip="123456")
    
    def test_create_user_with_same_phone(self):
        with self.assertRaises(Exception):
            Users.objects.create(username="test1", password="test1",
                                 email="whatever@gmail.com", phone='1234567890',
                                 address="test", city="test", state="test",
                                 country="test", zip="123456")
    
    def test_create_user_without_username(self):
        with self.assertRaises(Exception):
            Users.objects.create(password="test1", email="whatever@gmail.com",
                                 phone='1234567890', address="test",
                                 city="test", state="test", country="test",
                                 zip="123456")
    
    def test_working_app(self):
        response = self.client.get(reverse('working_app'))
        self.assertEqual(response.status_code, 200)

    def test_create_user_with_endpoint(self):
        data = {'password': 'test', 'username': 'test2', 'email': 'test2@gmail.com',
            'phone': '9876543210', 'address': 'test2', 'city': 'test2',
            'state': 'test2', 'country': 'test2', 'zip': '654321'}
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 201)
        
    def test_create_user_with_endpoint_with_same_email(self):
        data = {'password': 'test', 'username': 'test2', 'email': 'test2@gmail.com',
            'phone': '9876543210', 'address': 'test2', 'city': 'test2',
            'state': 'test2', 'country': 'test2', 'zip': '654321'}
        self.client.post(reverse('signup'), data)
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['message'], 'Check your email for activation link')
    
    def test_activate_user(self):
        resp = self.client.get(reverse('activate') + '?token=' + Users.objects.get(email="meemoo102039@gmail.com").activation_token)
        self.assertNotEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'User activated')
        self.assertEqual(Users.objects.get(email="meemoo102039@gmail.com").activated, True)
    
    def test_activate_user_with_invalid_token(self):
        resp = self.client.get(reverse('activate') + '?token=' + 'invalid_token')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'Invalid token')
    

from django.test import TestCase
from users.models import Users
from django.urls import reverse
from django.contrib.auth.hashers import check_password, make_password
# Create your tests here.


class UsersTestCase(TestCase):
    
    def setUp(self):
        passowrd = make_password("hardone")
        Users.objects.create(username="test", password=passowrd,
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

    def test_create_user_with_endpoint(self):
        password = 'thisisatestpassword'
        data = {'password': password, 'username': 'test2', 'email': 'test2@gmail.com',
            'phone': '9876543210', 'address': 'test2', 'city': 'test2',
            'state': 'test2', 'country': 'test2', 'zip': '654321'}
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 201)
    
    def test_hashed_password(self):
        password = 'thisisatestpassword'
        data = {'password': password, 'username': 'test2', 'email': 'test2@gmail.com',
            'phone': '9876543210', 'address': 'test2', 'city': 'test2',
            'state': 'test2', 'country': 'test2', 'zip': '654321'}
        self.client.post(reverse('signup'), data)
        user = Users.objects.get(email="test2@gmail.com")
        self.assertNotEqual(user.password, 'test')
    
    def test_missing_fields(self):
        data = {'password': 'test', 'username': 'test2', 'email': 'test2@gmail.com',
            'phone': '9876543210', 'city': 'test2',
            'state': 'test2', 'country': 'test2', 'zip': '654321'}
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 400)
        
    def test_create_user_with_endpoint_with_same_email(self):
        password = 'thisisatestpassword'
        data = {'password': password, 'username': 'test2', 'email': 'test2@gmail.com',
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
    
    def test_login_user(self):
        self.test_create_user_with_endpoint()
        self.client.get(reverse('activate') + '?token=' + Users.objects.get(email="test2@gmail.com").activation_token)
        data = {'email': 'test2@gmail.com', 'password': 'thisisatestpassword'}
        resp = self.client.post(reverse('login'), data)
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(resp.json()['token'], None)
        self.assertEqual(resp.json()['token'],
                         Users.objects.get(email="test2@gmail.com").session_token)
    
    def test_login_user_with_invalid_email(self):
        data = {'email': 'invalid', 'password': 'test'}
        resp = self.client.post(reverse('login'), data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'Invalid email')
    
    def test_logout_user(self):
        self.test_login_user()
        resp = self.client.post(reverse('logout'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['message'], 'User logged out')
    
    def test_forgot_passowrd(self):
        token = Users.objects.get(email='meemoo102039@gmail.com').reset_token
        self.assertEqual(token, None)
        resp = self.client.post(reverse('forgot_password'), {'email': 'meemoo102039@gmail.com'})
        token = Users.objects.get(email='meemoo102039@gmail.com').reset_token
        self.assertNotEqual(token, None)
        self.assertEqual(resp.json()['message'], 'Check your email for activation link')
    
    def test_change_forgot_password(self):
        self.test_forgot_passowrd()
        token = Users.objects.get(email='meemoo102039@gmail.com').reset_token
        passowrd = Users.objects.get(email='meemoo102039@gmail.com').password
        resp = self.client.post(reverse('reset_password'), {'token': token, 'password': 'new_password'})
        new_passowrd = Users.objects.get(email='meemoo102039@gmail.com').password
        self.assertNotEqual(passowrd, 'new_password')
        self.assertNotEqual(new_passowrd, 'new_password')
        self.assertEqual(check_password('new_password', new_passowrd), True)
        self.assertEqual(resp.json()['message'], 'Password changed')
        self.assertEqual(resp.status_code, 200)

    def test_get_user_profile(self):
        self.test_activate_user()
        resp = self.client.get(reverse('profile', args=['test']))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['status'], 'success')

    def test_get_user_not_exists(self):
        self.test_login_user()
        resp = self.client.get(reverse('profile', args=['username']))
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'No user found')

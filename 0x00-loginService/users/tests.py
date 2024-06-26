"""This file contains the test cases for the users app."""
from django.test import TestCase
from users.models import Users
from django.urls import reverse
from django.contrib.auth.hashers import check_password, make_password


class UsersTestCase(TestCase):
    """Test cases for the users app."""

    def setUp(self):
        """Create a user for testing."""
        passowrd = make_password("hardone")
        Users.objects.create(
            username="test",
            password=passowrd,
            email="meemoo102039@gmail.com",
            phone="1234567890",
            address="test",
            city="test",
            state="test",
            country="test",
            zip="123456")

    def test_user_create(self):
        """Test user creation."""
        self.assertEqual(Users.objects.count(), 1)
        user = Users.objects.get(username="test")
        self.assertEqual(user.username, "test")

    def test_user_update(self):
        """Test user update."""
        user = Users.objects.get(username="test")
        user.username = "test1"
        user.save()
        user = Users.objects.get(username="test1")
        self.assertNotEqual(user.username, None)

    def test_create_user_with_same_email(self):
        """Test creating user with same email."""
        with self.assertRaises(Exception):
            Users.objects.create(
                username="test1",
                password="test1",
                email="meemoo102039@gmail.com",
                phone="1234567890",
                address="test",
                city="test",
                state="test",
                country="test",
                zip="123456")

    def test_create_user_with_same_phone(self):
        """Test creating user with same phone."""
        with self.assertRaises(Exception):
            Users.objects.create(
                username="test1",
                password="test1",
                email="whatever@gmail.com",
                phone='1234567890',
                address="test",
                city="test",
                state="test",
                country="test",
                zip="123456")

    def test_create_user_without_username(self):
        """Test creating user without username."""
        with self.assertRaises(Exception):
            Users.objects.create(password="test1", email="whatever@gmail.com",
                                 phone='1234567890', address="test",
                                 city="test", state="test", country="test",
                                 zip="123456")

    def test_create_user_with_endpoint(self):
        """Test creating user with endpoint."""
        password = 'thisisatestpassword'
        data = {
            'password': password,
            'username': 'test2',
            'email': 'test2@gmail.com',
            'phone': '9876543210',
            'address': 'test2',
            'city': 'test2',
            'state': 'test2',
            'country': 'test2',
            'zip': '654321'}
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 201)

    def test_hashed_password(self):
        """Test hashed password"""
        password = 'thisisatestpassword'
        data = {
            'password': password,
            'username': 'test2',
            'email': 'test2@gmail.com',
            'phone': '9876543210',
            'address': 'test2',
            'city': 'test2',
            'state': 'test2',
            'country': 'test2',
            'zip': '654321'}
        self.client.post(reverse('signup'), data)
        user = Users.objects.get(email="test2@gmail.com")
        self.assertNotEqual(user.password, 'test')

    def test_missing_fields(self):
        """Test missing fields."""
        data = {
            'password': 'test',
            'username': 'test2',
            'email': 'test2@gmail.com',
            'phone': '9876543210',
            'city': 'test2',
            'state': 'test2',
            'country': 'test2',
            'zip': '654321'}
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 400)

    def test_create_user_with_endpoint_with_same_email(self):
        """Test creating user with same email."""
        password = 'thisisatestpassword'
        data = {
            'password': password,
            'username': 'test2',
            'email': 'test2@gmail.com',
            'phone': '9876543210',
            'address': 'test2',
            'city': 'test2',
            'state': 'test2',
            'country': 'test2',
            'zip': '654321'}
        self.client.post(reverse('signup'), data)
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['message'],
            'Check your email for activation link')

    def test_activate_user(self):
        """Test activating user."""
        resp = self.client.get(
            reverse('activate') +
            '?token=' +
            Users.objects.get(
                email="meemoo102039@gmail.com").activation_token)
        self.assertNotEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'User activated')
        self.assertEqual(
            Users.objects.get(
                email="meemoo102039@gmail.com").activated,
            True)

    def test_activate_user_with_invalid_token(self):
        """Test activating user with invalid token."""
        resp = self.client.get(
            reverse('activate') +
            '?token=' +
            'invalid_token')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'Invalid token')

    def test_login_user(self):
        """Test logging in user."""
        self.test_create_user_with_endpoint()
        self.client.get(
            reverse('activate') +
            '?token=' +
            Users.objects.get(
                email="test2@gmail.com").activation_token)
        data = {'email': 'test2@gmail.com', 'password': 'thisisatestpassword'}
        resp = self.client.post(reverse('login'), data)
        self.assertEqual(resp.status_code, 200)
        self.assertNotEqual(resp.json()['token'], None)
        self.assertEqual(
            resp.json()['token'], Users.objects.get(
                email="test2@gmail.com").session_token)

    def test_login_user_with_invalid_email(self):
        """Test logging in user with invalid email."""
        data = {'email': 'invalid', 'password': 'test'}
        resp = self.client.post(reverse('login'), data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'Invalid email')

    def test_logout_user(self):
        """Test logging out user."""
        self.test_login_user()
        resp = self.client.post(reverse('logout'))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['message'], 'User logged out')

    def test_forgot_passowrd(self):
        '''Test forgot password'''
        token = Users.objects.get(email='meemoo102039@gmail.com').reset_token
        self.assertEqual(token, None)
        resp = self.client.post(
            reverse('forgot_password'), {
                'email': 'meemoo102039@gmail.com'})
        token = Users.objects.get(email='meemoo102039@gmail.com').reset_token
        self.assertNotEqual(token, None)
        self.assertEqual(
            resp.json()['message'],
            'Check your email for activation link')

    def test_change_forgot_password(self):
        '''Test change forgot password'''
        self.test_forgot_passowrd()
        token = Users.objects.get(email='meemoo102039@gmail.com').reset_token
        passowrd = Users.objects.get(email='meemoo102039@gmail.com').password
        resp = self.client.post(
            reverse('reset_password'), {
                'token': token, 'password': 'new_password'})
        new_passowrd = Users.objects.get(
            email='meemoo102039@gmail.com').password
        self.assertNotEqual(passowrd, 'new_password')
        self.assertNotEqual(new_passowrd, 'new_password')
        self.assertEqual(check_password('new_password', new_passowrd), True)
        self.assertEqual(resp.json()['message'], 'Password changed')
        self.assertEqual(resp.status_code, 200)

    def test_get_user_profile(self):
        '''Test get user profile'''
        self.test_activate_user()
        resp = self.client.get(reverse('profile', args=['test']))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['status'], 'success')

    def test_get_user_not_exists(self):
        '''Test get user not exists'''
        self.test_login_user()
        resp = self.client.get(reverse('profile', args=['username']))
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'No user found')

    def test_update_user_profile(self):
        '''Test update user profile'''
        self.test_login_user()
        resp = self.client.post(
            reverse('update_profile'), {
                'username': 'new_username'})
        user = Users.objects.filter(username='new_username').first()
        self.assertEqual(resp.json()['message'], 'User updated')
        self.assertNotEqual(user, None)
        self.assertEqual(resp.status_code, 200)

    def test_delete_user_account(self):
        '''Test delete user account'''
        self.test_login_user()
        user = Users.objects.get(email='test2@gmail.com')
        self.assertNotEqual(user, None)
        resp = self.client.post(
            reverse('delete_acc'), {
                'password': 'thisisatestpassword'})
        self.assertEqual(resp.status_code, 200)
        user = Users.objects.filter(email='test2@gmail.com').first()
        self.assertEqual(user, None)

    def test_create_user_with_invalid_password(self):
        '''Test create user with invalid password'''
        password = 'weak'
        data = {
            'password': password,
            'username': 'test3',
            'email': 'test3@gmail.com',
            'phone': '9876543210',
            'address': 'test3',
            'city': 'test3',
            'state': 'test3',
            'country': 'test3',
            'zip': '123456'}
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 400)
        message = 'It must contain at least 8 characters.'
        self.assertEqual(
            response.json()['message'],
            f'This password is too short. {message}')

    def test_create_user_with_invalid_email_format(self):
        '''Test create user with invalid email format'''
        password = 'strongPassword123!'
        data = {
            'password': password,
            'username': 'test4',
            'email': 'invalid_email',
            'phone': '9876543210',
            'address': 'test4',
            'city': 'test4',
            'state': 'test4',
            'country': 'test4',
            'zip': '123456'}
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            response.json()['message'],
            'Enter a valid email address.')

    def test_login_with_inactive_user(self):
        '''Test login with inactive user'''
        self.test_create_user_with_endpoint()
        data = {'email': 'test2@gmail.com', 'password': 'thisisatestpassword'}
        resp = self.client.post(reverse('login'), data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'User not activated')

    def test_login_with_incorrect_password(self):
        '''Test login with incorrect password'''
        self.test_create_user_with_endpoint()
        self.client.get(
            reverse('activate') +
            '?token=' +
            Users.objects.get(
                email="test2@gmail.com").activation_token)
        data = {'email': 'test2@gmail.com', 'password': 'incorrectpassword'}
        resp = self.client.post(reverse('login'), data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'Invalid password')

    def test_logout_without_logging_in(self):
        '''Test logout without logging in'''
        resp = self.client.post(reverse('logout'))
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'User not logged in')

    def test_forgot_password_with_unregistered_email(self):
        '''Test forgot password with unregistered email'''
        data = {'email': 'unregistered_email@gmail.com'}
        resp = self.client.post(reverse('forgot_password'), data)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'Invalid email')

    def test_forgot_password_with_valid_email(self):
        '''Test forgot password with valid email'''
        self.test_create_user_with_endpoint()
        resp = self.client.post(
            reverse('forgot_password'), {
                'email': 'test2@gmail.com'})
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(
            resp.json()['message'],
            'Check your email for activation link')

    def test_reset_password_with_invalid_token(self):
        '''Test reset password with invalid token'''
        resp = self.client.post(
            reverse('reset_password'), {
                'token': 'invalid_token', 'password': 'new_password'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'Invalid token')

    def test_get_user_profile_unauthorized(self):
        '''Test get user profile unauthorized'''
        resp = self.client.get(reverse('profile', args=['test2']))
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'No user found')

    def test_update_profile_without_username(self):
        '''Test update profile without username'''
        self.test_login_user()
        resp = self.client.post(reverse('update_profile'), {})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'Username is required')

    def test_update_profile_with_invalid_fields(self):
        '''Test update profile with invalid fields'''
        self.test_login_user()
        resp = self.client.post(
            reverse('update_profile'), {
                'username': 'new_username', 'invalid_field': 'invalid'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'invalid field')

    def test_delete_user_account_without_password(self):
        '''Test delete user account without password'''
        self.test_login_user()
        resp = self.client.post(reverse('delete_acc'), {})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'password is required')

    def test_delete_user_account_with_invalid_password(self):
        '''Test delete user account with invalid password'''
        self.test_login_user()
        resp = self.client.post(
            reverse('delete_acc'), {
                'password': 'invalid_password'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'The password is Invalid')

    def test_delete_user_account_without_logging_in(self):
        '''Test delete user account without logging in'''
        resp = self.client.post(
            reverse('delete_acc'), {
                'password': 'thisisatestpassword'})
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['message'], 'Not logged in')

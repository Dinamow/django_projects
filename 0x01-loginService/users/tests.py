from django.test import TestCase
from users.models import Users
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
        

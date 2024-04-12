from django.http import JsonResponse
from users.models import Users
from django.shortcuts import render

# Create your views here.
def create_user(request):
    Users.objects.create(username="test", password="test",
                             email="meemoo102039@gmail.com", phone="1234567890",
                             address="test", city="test", state="test",
                             country="test", zip="123456")
    return JsonResponse({"status": "success"})


def all_users(request):
    users = Users.objects.all()
    return JsonResponse({"count": Users.objects.count(),
                         "users": list(users.values())})
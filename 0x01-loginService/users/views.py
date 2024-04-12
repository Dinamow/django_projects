from django.http import JsonResponse
from users.models import Users
from uuid import uuid4

# Create your views here.
def create_user(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"},
                            status=400)
    data = request.POST
    user = Users.objects.filter(email=data['email']).first()
    if user:
        if user.activated:
            return JsonResponse({"status": "error", "message": "Email already exists"},
                            status=400)
        else:
            return JsonResponse({"status": "error",
                                 "message": "Check your email for activation link"},
                                status=400)
    try:
        Users.objects.create(username=data['username'], password=data['password'],
                             email=data['email'], phone=data['phone'],
                             address=data['address'], city=data['city'],
                             state=data['state'], country=data['country'],
                             zip=data['zip'])
        return JsonResponse({"status": "success", "message": "User created"},
                            status=201)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

def all_users(request):
    users = Users.objects.all()
    return JsonResponse({"count": Users.objects.count(),
                         "users": list(users.values())})

def working_app(request):
    return JsonResponse({"status": "success"})
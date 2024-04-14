from django.http import JsonResponse
from users.models import Users
from django.shortcuts import redirect
from uuid import uuid4
from bcrypt import hashpw, gensalt


requered_fields = ['username', 'password', 'email', 'phone', 'address', 'city',
                   'state', 'country', 'zip']


# Create your views here.
def create_user(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"},
                            status=400)
    data = request.POST
    for field in requered_fields:
        if not data.get(field):
            return JsonResponse({"status": "error", "message": f"{field} is required"},
                                status=400)
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
        passowrd = hashpw(data['password'].encode(), gensalt())
        user = Users.objects.create(username=data['username'], password=passowrd,
                                    email=data['email'], phone=data['phone'],
                                    address=data['address'], city=data['city'],
                                    state=data['state'], country=data['country'],
                                    zip=data['zip'], activation_token=str(uuid4()))
        return JsonResponse({"status": "success", "message": "User created",
                             "activation_token": user.activation_token},
                            status=201)
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

def all_users(request):
    users = Users.objects.all()
    return JsonResponse({"count": Users.objects.count(),
                         "users": list(users.values())})

def working_app(request):
    return JsonResponse({"status": "success"})

def activate_user(request):
    user = Users.objects.filter(activation_token=request.GET.get('token')).first()
    if not user:
        return JsonResponse({"status": "error", "message": "Invalid token"},
                            status=400)
    user.activated = True
    user.save()
    return JsonResponse({"status": "success", "message": "User activated"})

def login_user(request):
    pass
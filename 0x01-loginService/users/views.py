from django.http import JsonResponse
from users.models import Users
from uuid import uuid4
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.password_validation import validate_password


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
        validate_password(data['password'])
        passowrd = make_password(data['password'])
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
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"},
                            status=400)
    data = request.POST
    if not data.get('email') or not data.get('password'):
        return JsonResponse({"status": "error", "message": "Email and password are required"},
                            status=400)
    user = Users.objects.filter(email=data['email']).first()
    if not user:
        return JsonResponse({"status": "error", "message": "Invalid email"},
                            status=400)
    if not user.activated:
        return JsonResponse({"status": "error", "message": "User not activated"},
                            status=400)
    if not check_password(data['password'], user.password):
        return JsonResponse({"status": "error", "message": "Invalid password"},
                            status=400)
    user.session_token = str(uuid4())
    request.session['session_id'] = user.session_token
    user.save()
    return JsonResponse({"status": "success", "message": "User logged in",
                         "token": user.session_token})
    
def logout_user(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"},
                            status=400)
    if not request.session.get('session_id'):
        return JsonResponse({"status": "error", "message": "User not logged in"},
                            status=400)
    user = Users.objects.filter(session_token=request.session['session_id']).first()
    if not user:
        return JsonResponse({"status": "error", "message": "User not logged in"},
                            status=400)
    request.session['session_id'] = None
    user.session_token = ''
    user.save()
    return JsonResponse({"status": "success", "message": "User logged out"})

def forgot_password(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"},
                            status=400)
    email = request.POST.get('email')
    if not email:
        return JsonResponse({"status": "error", "message": "Email is required"},
                            status=400)
    user = Users.objects.filter(email=email).first()
    if not user:
        return JsonResponse({"status": "error", "message": "Invalid email"},
                            status=400)
    user.reset_token = str(uuid4())
    user.save()
    return JsonResponse({"status": "success", "message": "Check your email for activation link"})

def reset_password(request):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request"},
                            status=400)
    data = request.POST
    if not data.get('token') or not data.get('password'):
        return JsonResponse({"status": "error", "message": "Token and password are required"},
                            status=400)
    user = Users.objects.filter(reset_token=data['token']).first()
    if not user:
        return JsonResponse({"status": "error", "message": "Invalid token"},
                            status=400)
    try:
        validate_password(data['password'])
        user.password = make_password(data['password'])
        user.save()
        return JsonResponse({"status": "success", "message": "Password changed"})
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

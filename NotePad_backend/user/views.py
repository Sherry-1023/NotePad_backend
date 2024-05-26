from django.http import JsonResponse
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from .models import User
import json
 
def index(request):
    return HttpResponse('Hello world!')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            # 尝试解析 JSON 请求体
            data = json.loads(request.body.decode('utf-8'))
            user_name = data.get('username')
            pass_word = data.get('password')
        except (json.JSONDecodeError, AttributeError, TypeError):
            # 如果解析失败，返回一个 Bad Request 响应
            return HttpResponseBadRequest("Invalid JSON")

        # 根据用户名获取用户对象
        try:
            user = User.objects.get(username=user_name)
            # 注意：实际应用中不应该直接比较明文密码，而应该使用django的密码验证机制
            pwd = user.password
        except User.DoesNotExist:
            user = None

        # 如果用户存在且密码匹配，则返回成功信息
        if user and pass_word == pwd:
            # login(request, user)  # 实际应用中，应该使用这个函数来完成用户登录
            return JsonResponse({'message': 'User logged in successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        try:
        # 从POST请求中获取注册信息
            data = json.loads(request.body.decode('utf-8'))
            user_name = data.get('username')
            pass_word = data.get('password')

        except (json.JSONDecodeError, AttributeError, TypeError):
            # 如果解析失败，返回一个 Bad Request 响应
            return HttpResponseBadRequest("Invalid JSON")

        # 检查用户名是否已经存在
        if User.objects.filter(username=user_name).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)
        
        # 创建新用户
        User.objects.create(
            username=user_name,
            password=pass_word  # 使用make_password加密密码
        )

        # query_user = User.objects.values('username')
        # query_user = User.objects.values_list('username', 'password')
        # print(query_user)
        # User.objects.all().delete()


        return JsonResponse({'message': 'User registered successfully'}, status=200)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
@csrf_exempt
def userinfo(request):
    
    pass
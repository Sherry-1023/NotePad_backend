from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from .models import User

 
def index(request):
    return HttpResponse('Hello world!')

@csrf_exempt
def login(request):
    if request.method == 'POST':
        # 从POST请求中获取登录信息
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')

        # 根据用户名获取用户对象
        try:
            user = User.objects.get(username=user_name)
            pwd = user.password
        except User.DoesNotExist:
            user = None 

        # 如果用户存在且密码匹配，则登录用户
        if user and pass_word == pwd:
            # 登录用户
            # login(request, user)
            return JsonResponse({'message': 'User logged in successfully'}, status=200)
        else:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)

@csrf_exempt
def register(request):
    if request.method == 'POST':
        # 从POST请求中获取注册信息
        user_name = request.POST.get('username')
        pass_word = request.POST.get('password')

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


        return JsonResponse({'message': 'User registered successfully'}, status=201)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
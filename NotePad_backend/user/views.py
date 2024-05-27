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
def login_in(request):
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
            pwd = user.password
        except User.DoesNotExist:
            user = None

        # 如果用户存在且密码匹配，则返回成功信息
        if user and pass_word == pwd:
            # login(request, user)  
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
def modify_pwd(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_name = data.get('username')
            origin_pwd = data.get('origin_pwd')
            pass_word = data.get('password')
            
        
        except (json.JSONDecodeError, AttributeError, TypeError):
            # 如果解析失败，返回一个 Bad Request 响应
            return HttpResponseBadRequest("Invalid JSON")
        
        # 用户名存在
        if User.objects.filter(username=user_name).exists():
            user = User.objects.get(username=user_name)
            if origin_pwd == user.password:
                user.password = pass_word
            else:
                return JsonResponse({'error': 'The original password is not correct'}, status=400)
            user.save()
            
            # query_user = User.objects.values_list('username', 'password')
            # print(query_user)
            
            return JsonResponse({'message': 'Password modified successfully'}, status=200)
        else:
            return JsonResponse({'error': 'User does not exist'}, status=404)
    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def userinfo(request):
    if request.method == 'GET':
        user_name = request.GET.get('username')

        if not user_name:
            return HttpResponseBadRequest("Username is required")

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        user_info = {
            'username': user.username,
            'avatar': user.avatar.url if user.avatar else '',
            'nickname': user.nickname,
            'bio': user.bio,
        }
        return JsonResponse({'userinfo': user_info}, status=200)

    elif request.method == 'POST':
        user_name = request.POST.get('username')
        avatar_ = request.FILES.get('avatar')  # Use request.FILES for file uploads
        nick_name = request.POST.get('nickname')
        bio_ = request.POST.get('bio')

        if not user_name:
            return HttpResponseBadRequest("Username is required")

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        if avatar_:
            user.avatar = avatar_
        if nick_name:
            user.nickname = nick_name
        if bio_:
            user.bio = bio_
        user.save()
        # query_user = User.objects.values('username')
        query_user = User.objects.values_list('username', 'password', 'nickname', 'bio')
        print(query_user)
        # User.objects.all().delete()

        return JsonResponse({'message': 'User information updated successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Only GET and POST requests are allowed'}, status=405)
    
@csrf_exempt
def noteinfo(request):
    if request.method == 'GET':
        user_name = request.GET.get('username')

        if not user_name:
            return HttpResponseBadRequest("Username is required")
        
        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)
        
        #TODO
        note_info = {
            'username': user.username,
        }
        return JsonResponse({'noteinfo': note_info}, status=200)

    elif request.method == 'POST':
        #TODO
        return JsonResponse({'message': 'Note information updated successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Only GET and POST requests are allowed'}, status=405)
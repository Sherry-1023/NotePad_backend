from django.http import JsonResponse, Http404
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
# from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login
from django.shortcuts import get_object_or_404
from .models import User, Note
import json
import logging
from django.db.models import Q

import base64
from django.core.files.base import ContentFile

def index(request):
    return HttpResponse('Hello world!')
logger = logging.getLogger(__name__)
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

        avatar_base64 = ''
        if user.avatar:
            avatar_base64 = base64.b64encode(user.avatar.read()).decode('utf-8')
            # print("Avatar Base64:", avatar_base64)  # 打印Base64编码的头像字符串
            

        user_info = {
            'username': user.username,
            'avatar': avatar_base64,
            'nickname': user.nickname,
            'bio': user.bio,
        }
        return JsonResponse({'userinfo': user_info}, status=200)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_name = data.get('username')
            avatar_base64 = data.get('avatar')
            nick_name = data.get('nickname')
            bio_ = data.get('bio')
        except (json.JSONDecodeError, AttributeError, TypeError) as e:
            return HttpResponseBadRequest("Invalid JSON")

        if not user_name:
            return HttpResponseBadRequest("Username is required")

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        if avatar_base64:
            try:
                # 检查是否包含 ';base64,'
                if ';base64,' in avatar_base64:
                    format, imgstr = avatar_base64.split(';base64,')
                    ext = format.split('/')[-1]
                else:
                    imgstr = avatar_base64
                    # 设置默认的扩展名为 'png'，你可以根据实际情况调整
                    ext = 'png'

                # 尝试解码并保存图片
                avatar = ContentFile(base64.b64decode(imgstr), name=f'{user_name}.{ext}')
                user.avatar = avatar
            except Exception as e:
                print("Exception occurred while decoding base64 image:", str(e))
                return HttpResponseBadRequest("Invalid base64 image format")
        else:
            print("avatar_base64 is empty or None")
            return HttpResponseBadRequest("No image provided")
        
        if nick_name:
            user.nickname = nick_name
        if bio_:
            user.bio = bio_
        
        user.save()

        return JsonResponse({'message': 'User information updated successfully'}, status=200)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)


@csrf_exempt
def noteinfo(request):
    if request.method == 'GET':
        user_name = request.GET.get('username')
        tag_query = request.GET.get('tag')  # 获取标签查询参数

        if not user_name:
            return HttpResponseBadRequest("Username is required")
        
        user = get_object_or_404(User, username=user_name)
        notes = user.notes.all()
        
        if tag_query:
            notes = notes.filter(tags__icontains=tag_query)  # 过滤包含指定标签的笔记
        
        notes_info = [
            {
                'id': note.id,
                'title': note.title,
                'tags': note.tags,
                'content': note.content
            }
            for note in notes
        ]
        
        # Note.objects.all().delete()

        return JsonResponse({'notes': notes_info}, status=200)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)
@csrf_exempt
def searchnotes(request):
    if request.method == 'GET':
        query = request.GET.get('query')
        user_name = request.GET.get('username')

        if not query or not user_name:
            return HttpResponseBadRequest("Query and username are required")

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        notes = user.notes.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        )

        notes_info = [
            {
                'id': note.id,
                'title': note.title,
                'tags': note.tags,
                'content': note.content,
            }
            for note in notes
        ]

        return JsonResponse({'notes': notes_info}, status=200)
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)


@csrf_exempt
def notedetail(request):
    if request.method == 'GET':
        note_id = request.GET.get('note_id')

        if not note_id:
            return HttpResponseBadRequest("Note ID is required")

        note = get_object_or_404(Note, id=note_id)
        note_detail = {
            'title': note.title,
            'tags': note.tags,
            'content': note.content
        }
        # 处理图像
        if note.image:
            image_base64 = base64.b64encode(note.image.read()).decode('utf-8')
            note_detail['image'] = image_base64

        # 处理音频
        if note.audio:
            audio_base64 = base64.b64encode(note.audio.read()).decode('utf-8')
            note_detail['audio'] = audio_base64
        # query_user = Note.objects.values_list('title', 'content', 'image')
        # print(query_user)
        return JsonResponse({'notedetail': note_detail}, status=200)

    elif request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            note_id = data.get('note_id')
            title_ = data.get('title')
            tags_ = data.get('tags')
            content_ = data.get('content')
            image_base64 = data.get('image')
            audio_base64 = data.get('audio')
        except (json.JSONDecodeError, AttributeError, TypeError) as e:
            return HttpResponseBadRequest("Invalid JSON")

        if not note_id:
            return HttpResponseBadRequest("Note ID is required")

        try:
            note = Note.objects.get(id=note_id)
        except Note.DoesNotExist:
            return JsonResponse({'error': 'Note does not exist'}, status=404)

        if title_:
            note.title = title_
        if tags_:
            note.tags = tags_
        if content_:
            note.content = content_

        if image_base64:
            try:
                if ';base64,' in image_base64:
                    format, imgstr = image_base64.split(';base64,')
                    ext = format.split('/')[-1]
                else:
                    imgstr = image_base64
                    ext = 'png'

                image = ContentFile(base64.b64decode(imgstr), name=f'{note_id}_image.{ext}')
                note.image = image
            except Exception as e:
                # print("Exception occurred while decoding base64 image:", str(e))
                return HttpResponseBadRequest("Invalid base64 image format")

        if audio_base64:
            try:
                if ';base64,' in audio_base64:
                    format, audstr = audio_base64.split(';base64,')
                    ext = format.split('/')[-1]
                else:
                    audstr = audio_base64
                    ext = 'mp3'

                audio = ContentFile(base64.b64decode(audstr), name=f'{note_id}_audio.{ext}')
                note.audio = audio
            except Exception as e:
                # print("Exception occurred while decoding base64 audio:", str(e))
                return HttpResponseBadRequest("Invalid base64 audio format")

        note.save()
        return JsonResponse({'message': 'Note updated successfully'}, status=200)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
@csrf_exempt
def createnote(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body.decode('utf-8'))
            user_name = data.get('username')
            title_ = data.get('title')
            tags_ = data.get('tags')
            content_ = data.get('content')
            image_base64 = data.get('image')
            audio_base64 = data.get('audio')
        except (json.JSONDecodeError, AttributeError, TypeError) as e:
            return HttpResponseBadRequest("Invalid JSON")

        if not user_name or not title_ or not content_:
            return HttpResponseBadRequest("Username, title, and content are required")

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        note = Note(
            user=user,
            title=title_,
            tags=tags_ if tags_ else '',
            content=content_
        )

        if image_base64:
            try:
                if ';base64,' in image_base64:
                    format, imgstr = image_base64.split(';base64,')
                    ext = format.split('/')[-1]
                else:
                    imgstr = image_base64
                    ext = 'png'

                image = ContentFile(base64.b64decode(imgstr), name=f'{user_name}_image.{ext}')
                note.image = image
            except Exception as e:
                # print("Exception occurred while decoding base64 image:", str(e))
                return HttpResponseBadRequest("Invalid base64 image format")

        if audio_base64:
            try:
                if ';base64,' in audio_base64:
                    format, audstr = audio_base64.split(';base64,')
                    ext = format.split('/')[-1]
                else:
                    audstr = audio_base64
                    ext = 'mp3'

                audio = ContentFile(base64.b64decode(audstr), name=f'{user_name}_audio.{ext}')
                note.audio = audio
            except Exception as e:
                # print("Exception occurred while decoding base64 audio:", str(e))
                return HttpResponseBadRequest("Invalid base64 audio format")

        note.save()

        return JsonResponse({'message': 'Note created successfully', 'note_id': note.id}, status=201)

    else:
        return JsonResponse({'error': 'Only POST requests are allowed'}, status=405)
    
@csrf_exempt
def deletenote(request):
    if request.method == 'GET':
        note_id = request.GET.get('note_id')
        user_name = request.GET.get('username')

        if not user_name or not note_id:
            return HttpResponseBadRequest("Username and note ID are required")

        try:
            user = User.objects.get(username=user_name)
        except User.DoesNotExist:
            return JsonResponse({'error': 'User does not exist'}, status=404)

        try:
            note = Note.objects.get(id=note_id, user=user)
        except Note.DoesNotExist:
            return JsonResponse({'error': 'Note does not exist or does not belong to this user'}, status=404)

        note.delete()
        return JsonResponse({'message': 'Note deleted successfully'}, status=200)
    
    else:
        return JsonResponse({'error': 'Only GET requests are allowed'}, status=405)

@csrf_exempt
def get_avatar(request, username):
    user = get_object_or_404(User, username=username)
    if user.avatar:
        response = HttpResponse(user.avatar, content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename={user.avatar.name}'
        return response
    else:
        raise Http404("Avatar not found")


@csrf_exempt
def get_note_image(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.image:
        response = HttpResponse(note.image, content_type='image/jpeg')
        response['Content-Disposition'] = f'attachment; filename={note.image.name}'
        return response
    else:
        raise Http404("Image not found")

@csrf_exempt
def get_note_audio(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.audio:
        response = HttpResponse(note.audio, content_type='audio/mpeg')
        response['Content-Disposition'] = f'attachment; filename={note.audio.name}'
        return response
    else:
        raise Http404("Audio not found")

@csrf_exempt
def get_note_video(request, note_id):
    note = get_object_or_404(Note, id=note_id)
    if note.video:
        response = HttpResponse(note.video, content_type='video/mp4')
        response['Content-Disposition'] = f'attachment; filename={note.video.name}'
        return response
    else:
        raise Http404("Video not found")
# NotePad_backend
THU移动应用软件开发2024春大作业后端代码

## 运行
使用以下命令运行
```py
python manage.py runserver
```

### 数据传输格式
`username`为用户唯一标识。
`url`如下：
```py
urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_in, name='login'),
    path('userinfo/', views.userinfo, name='userinfo'),
    path('noteinfo/', views.noteinfo, name='noteinfo'),
    path('modify/', views.modify_pwd, name='modify'),
    path('notedetail/', views.notedetail, name='notedetail'),
    path('createnote/', views.createnote, name='createnote'),
]
```

#### 登录
已完成
#### 注册
已完成
#### 个人信息
用户名、头像、昵称、个人简介。
GET:
```json
{
    "userinfo": {
        "username": "string",
        "avatar": "url",
        "nickname": "string",
        "bio": "string"
    }
}
```
POST:
```json
{
    "username":"string",
    "avatat":"url",
    "nickname":"string",
    "bios":"string"
}
```
#### 密码修改
用户名、原密码、新密码
```json
{
    "username":"string",
    "origin_pwd":"string",
    "password":"string"
}
```
#### 笔记
**新建笔记(createnote):** 新建一个笔记，note_id是笔记的唯一标识
**POST:**
request:
```json
{
    "username": "string",
    "title": "string",
    "tags": "string",
    "content": "string",
    "image": "url",
    "audio": "url",
    "video": "url"
}
```

response:
```json
{
    "note_id": int
}
```

**笔记主页(noteinfo)：** 显示当前用户的所有笔记（搜索还未完成），每一个笔记显示这个笔记的title, content（前端显示可能只要显示前面的字）, tags（需要显示吗？）

**GET：**
request:
```json
{
    "username":"string"
}
```

response:
```json
{
    "notes": [
        {
            "title": "string",
            "tags": "string",
            "content": "string"
        }
    ]
}
```

**笔记详情(notedetail):** 显示某个笔记的特定内容，包含笔记的所有信息。

**GET:**
request:
```json
{
    "note_id":int
}
```

response:
```json
{
    "notedetail": {
        "title": "string",
        "tags": "string",
        "content": "string",
        "image": "url",
        "audio": "url",
        "video": "url"
    }
}
```

**POST:**  note_id是必须项
request:
```json
{
    "note_id": int,
    "title": "string",
    "tags": "string",
    "content": "string",
    "image": "url",
    "audio": "url",
    "video": "url"
}
```

response:
```json
{
    "notedetail": {
        "title": "string",
        "tags": "string",
        "content": "string",
        "image": "url",
        "audio": "url",
        "video": "url"
    }
}
```

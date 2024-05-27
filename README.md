# NotePad_backend
THU移动应用软件开发2024春大作业后端代码

## 运行
使用以下命令运行
```py
python manage.py runserver
```

### 数据传输格式
`username`为用户唯一标识。
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
#### 笔记本
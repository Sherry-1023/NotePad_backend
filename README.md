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
#### 笔记
分为笔记主页和详情页

**笔记主页：** 显示当前用户的所有笔记，每一个笔记在主页仅仅显示标题、内容、标签，内容可能需要进行截断只显示一部分（前端），标签前端是否显示？

接口如下，仅支持GET方法：

request
```json

```
response
```json

```
**笔记详情：** 

"""
URL configuration for NotePad_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from user import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login_in, name='login'),
    path('userinfo/', views.userinfo, name='userinfo'),
    path('noteinfo/', views.noteinfo, name='noteinfo'),
    path('modify_pwd/', views.modify_pwd, name='modify'),
    path('notedetail/', views.notedetail, name='notedetail'),
    path('searchnotes/', views.searchnotes, name='searchnotes'),
    path('createnote/', views.createnote, name='createnote'),
    path('deletenote/', views.deletenote, name='deletenote'),
    path('user/<str:username>/avatar/', views.get_avatar, name='get_avatar'),
    path('notes/<int:note_id>/image/', views.get_note_image, name='get_note_image'),
    path('notes/<int:note_id>/audio/', views.get_note_audio, name='get_note_audio'),
    path('notes/<int:note_id>/video/', views.get_note_video, name='get_note_video'),
]

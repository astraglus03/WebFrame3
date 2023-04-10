from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('about_me/', views.about_me),
    path('', views.landing), #아무것도 안넣었을 경우 landing호출
]

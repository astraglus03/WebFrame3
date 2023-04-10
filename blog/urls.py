from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    path('',views.index),
    path('<int:pk>/', views.single_post_page) # pk는 변수
]
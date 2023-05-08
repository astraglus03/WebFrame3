from django.contrib import admin
from django.urls import path, include
from . import views
urlpatterns = [
    # path('blog/', include('blog.urls')),
    path("", views.index),
    path('prob/',views.St_List.as_view()),
    path('prob/<int:pk>/',views.St_Detail.as_view()),
    # path('',include('single_pages.urls')),
    # path('exam/',include('exam.urls')),
]
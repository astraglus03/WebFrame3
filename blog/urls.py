from django.urls import path
from . import views

urlpatterns=[
    # 이 부분을 채울 예정!

    path('',views.PostList.as_view()),
    # path('', views.index),
    path('<int:pk>/',views.PostDetail.as_view()) # pk는 변수
    # path('<int:pk>/', views.single_post_page),
]
from django.urls import path
from . import views

urlpatterns=[
    # 이 부분을 채울 예정!
    path('search/<str:q>/',views.PostSearch.as_view()),
    path('<int:pk>/new_comment/', views.new_comment),
    path('update_comment/<int:pk>/',views.CommentUpdate.as_view()),
    path('delete_comment/<int:pk>/',views.delete_comment),
    path('',views.PostList.as_view()),
    # path('', views.index),
    path('<int:pk>/',views.PostDetail.as_view()), # pk는 변수
    # path('<int:pk>/', views.single_post_page),
    path('category/<str:slug>/', views.category_page), # category_page 함수 호출   as_view가 있으면 class 없으면 함수.
    path('create_post/',views.PostCreate.as_view()), # PostCreate 클래스를 참조해라.
    path('update_post/<int:pk>/',views.PostUpdate.as_view()),
]
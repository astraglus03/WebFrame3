from django.shortcuts import render
from .models import Post
from django.views.generic import ListView,DetailView
# Create your views here.

#CBV
class PostList(ListView):
    model=Post
    ordering='-pk'
    template_name='blog/post_list.html'


# FBV
# def index(request):
#     posts = Post.objects.all().order_by('-pk')  # -사용시 내림차순, 없을시 오름차순 pk는 primary key의 약자를 의미함
#
#     return render(
#         request,
#         'blog/post_list.html',
#         {
#             'posts': posts,
#         }
#     )

class PostDetail(DetailView):
    model=Post
    # template_name='blog/single_post_page.html'


# def single_post_page(request, pk):
#     post = Post.objects.get(pk=pk) # objects.get은 괄호안에 만족하는 레코드를 가져오라는 의미이다.
#
#     return render(
#         request,
#         'blog/index.html',
#         {
#             'post':post,
#         }
#     )
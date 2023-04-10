from django.shortcuts import render
from .models import Post
# Create your views here.

def index(request):
    posts=Post.objects.all().order_by('pk') # db 테이블에 저장되어있는 레코드(objects) -는 역순으로 가져온다는 의미(내림차순) -없으면 오름차순

    return render(
        request,
        'blog/index.html',
        {
            'posts': posts,
        }
    )

def single_post_page(request,pk):
    post=Post.objects.get(pk=pk)
    return render(
        request,
        'blog/single_post_page.html',
        {
            'post': post,
        }
    )
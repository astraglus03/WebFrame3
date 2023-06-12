from django.shortcuts import render
from blog.models import Post
# Create your views here.

def landing(request):
    recent_posts = Post.objects.order_by('-pk')[:3]
    return render(
        request,
        'single_pages/landing.html', # templates 에서 만들어줘야함. / 그냥 single_pages바로 아래에 만들면 안됌!
        {
            'recent_posts':recent_posts
        }
    )

def about_me(request):
    return render(
        request,
        'single_pages/about_me.html',
    )

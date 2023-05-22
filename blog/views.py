from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
# Create your views here.

def csrf_failure(request,reason=""):
    return redirect('/blog/')

# CBV
class PostList(ListView):
    model = Post
    ordering = '-pk'
    template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()  # post_list를 가져옴 # 상위에서 가져오기때문
        context['categories'] = Category.objects.all()  # Category DB의 내용
        context['no_category_post_count'] = Post.objects.filter(
            category=None).count()  # category가 없을수 있기때문에 no_category이고 뒤에는 없는것 카운트
        return context  # => 리턴은 post_list.html로 들어가게된다.


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
    model = Post

    # template_name='blog/single_post_page.html'
    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()  # post_list를 가져옴 # 상위에서 가져오기때문
        context['categories'] = Category.objects.all()  # Category DB의 내용
        context['no_category_post_count'] = Post.objects.filter(
            category=None).count()  # category가 없을수 있기때문에 no_category
        return context  # => 리턴은 post_detail.html로 들어가게된다. (post.categories,no_category_post_count) 값이 넘어가게됌.


def category_page(request, slug):  # 프로그래밍, 문화-예술, 웹개발, 미분류 -> no_category로 가게됌
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None) # .all()
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )

# /blog/create_post/
class PostCreate(LoginRequiredMixin,UserPassesTestMixin, CreateView): # UserPassesTestMixin <- 유저가 로그인 되어있는지 확인하는 것.

    model=Post
    fields=['title','hook_text','content', 'head_image', 'file_upload', 'category','tags']
    # template_name=post_form.html {form}

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff # user가 관리자 계정 or 스태프인지 확인후 접근가능 -> create_post 접근

    def form_valid(self,form):
        current_user=self.request.user # 로그인 되어있는 유저 / 로그인안하면 null
        if(current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser)): # 로그인만 할지 슈퍼유저,스태프까지 할지 결정. 지워도 됌.
            form.instance.author=current_user
            # 유저를 안채울거면 없어도 된다.
            # not tag
            return super(PostCreate,self).form_valid(form) # 상위 생성자 호출하기.
        else:
            return redirect('/blog/') # 강제적으로 '/blog/'로 보내버림

# blog/update_post/<int:pk>
class PostUpdate(LoginRequiredMixin,UpdateView):
    model=Post
    fields=['title','hook_text','content', 'head_image', 'file_upload', 'category','tags']

    # 기본 템플릿 이름: post_form.html // 위에 PostCreate와 공유를 하게 되서 문제 발생 그래서 다른 템플릿 적용
    template_name= "blog/post_update_form.html"

    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author: # self.get_object() detail에서 글까지 보여주는 부분이고 그 작성자가 앞에랑 같냐고 하는 코드
            return super (PostUpdate,self).dispatch(request,*args,**kwargs)
        else:
            return PermissionDenied





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

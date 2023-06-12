# context를 넣어서 보내는 건 views.py!
from django.db.models import Q
from django.shortcuts import render, redirect
from .models import Post, Category, Tag
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from .forms import CommentForm, Comment
from django.shortcuts import get_object_or_404  # db에서 하나만 가져오는 명령어


# Create your views here.

# CBV
class PostList(ListView):  # 그냥 안 돌아가서 urls 파일로 가서 바꿔야 함
    model = Post  # post_list
    ordering = '-pk'  # 최신 글부터 보이게 함
    paginate_by = 2  # 한페이지에 몇개씩 보여줄지 결정함

    # template_name = 'blog/index.html' #템플릿 name을 정의하지 않으면 클래스 명을 파일 이름으로 바꿔서 자동으로 찾음
    # 1.내가 이름을 바꿔서 지정하거나, 자동으로 연결되는 이름으로 다른 걸 바꾸던가(우린 후자)
    # template_name = 'blog/post_list.html'

    def get_context_data(self, **kwargs):
        context = super(PostList, self).get_context_data()  # post_list를 가져옴 # 상위에서 가져오기때문
        context['categories'] = Category.objects.all()  # Category DB의 내용
        context['no_category_post_count'] = Post.objects.filter(
            category=None).count()  # category가 없을수 있기때문에 no_category이고 뒤에는 없는것 카운트
        return context  # => 리턴은 post_list.html로 들어가게된다.


# FBV
# == 위 클래스 이용하는 거랑 같음. 아래는 직접 코드를 써서 하는 방법
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
    # 여기는 템플릿 이름을 정의하지 않아서, 자동으로 post.html?을 자동으로 찾음
    # template_name = post_form.html  #post_detail.html로 이름 바꿔서 주석처리하면 자동으로 이름 바뀜

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()  # post_list를 가져옴 # 상위에서 가져오기 때문
        context['categories'] = Category.objects.all()  # Category DB의 내용
        context['no_category_post_count'] = Post.objects.filter(
            category=None).count()  # category가 없을 수 있기 때문에 no_category
        # 필터: 검색 조건, count 몇 개가 들어있는지 세는 것
        context['comment_form'] = CommentForm
        return context  # => 리턴은 post_detail.html로 들어가게 된다. (post.categories,no_category_post_count) 값이 넘어가게 됨.


def category_page(request, slug):  # 프로그래밍, 문화-예술, 웹개발, 미분류 -> no_category로 가게됌
    if slug == 'no_category':
        category = '미분류'
        post_list = Post.objects.filter(category=None)  # post_list = Post.objects.all()이었다면 모든 리스트가 다 나옴
    else:
        category = Category.objects.get(slug=slug)
        post_list = Post.objects.filter(category=category)

    return render(
        request,
        'blog/post_list.html',
        {  # context 넣는 위치! 알기 '변수명 : 들어갈 내용'
            # 필터링한 것만 뜨게 하기
            'post_list': post_list,
            'categories': Category.objects.all(),
            'no_category_post_count': Post.objects.filter(category=None).count(),
            'category': category,
        }
    )


# /blog/create_post/
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):  # form
    # UserPassesTestMixin : 특정 사용자만 접근을 허용하기

    model = Post  # CreateView임
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    # template_name=post_form.html

    def test_func(self):  # UserPassesTestMixin에서 확인할 조건 : 최고권한(super user) 혹은 스태프(staff) 인 경우
        return self.request.user.is_superuser or self.request.user.is_staff

    def form_valid(self, form):  # CreateView에서 생성된 form이 제대로 입력되었는지 확인하는 함수
        current_user = self.request.user
        # 로그인을 했느냐 and 스태프나 관리자 계정이냐 (필요에 따라 하나 지워도 됨)
        if (current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser)):
            form.instance.author = current_user
            # not tag
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('/blog/')  # 강제적으로 '/blog/'로 보내버림


# 토큰이 검증이 안 될 때 함수 실행 #관리자가 아닌 사용자한테 굳이 메시지를 띄울 필요는 없음.
# 에러 메시지 안 띄우고 바로 이전 페이지로 가게 하기
def crsf_failure(request, reason=""):
    return redirect('/blog/')


# blog/update_post/pk/
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['title', 'hook_text', 'content', 'head_image', 'file_upload', 'category', 'tags']

    # post_form.html이 기본 템플릿. 그래서 edit 버튼 누르면 create new post 템플릿과 공유를 하게 됨. 수정 화면인데 생성 포스트 화면으로 뜸
    # -> 똑같은데 다른 템플릿을 만들고, 다른 템플릿 이름을 쓰면 됨.
    # post_form.html 복붙하고 이름 바꾸기
    template_name = "blog/post_update_form.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:  # 현재 화면에 보이는 포스트 글이 가져와짐
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied  # 에러 404

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


def new_comment(request, pk):
    if request.user.is_authenticated:  # 댓글은 로그인 됐을 때만 작성 가능
        post = get_object_or_404(Post, pk=pk)

        if request.method == "POST":
            comment_form = CommentForm(request.POST)  # 댓글 작성하는 폼
            if comment_form.is_valid():  # 이 폼이 정상적이라면
                comment = comment_form.save(commit=False)  # 임시저장
                comment.post = post  # 현재 포스트
                comment.author = request.user  # 현재 user(로그인 된) #modify는 자동으로 save
                comment.save()  # save된 걸 불러옴?
                return redirect(comment.get_absolute_url())  # 이 포스트로 돌아가라

        else:
            return redirect(post.get_absolute_url())  # 주소에 바로 /new_comment/ 쳤을 땐 blog 페이지로 이동할 수 있도록
    else:  # 로그인 안 됐을 땐 권한이 없다고 할 것임.
        raise PermissionDenied


def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post
    if request.user.is_authenticated and request.user == comment.author:
        comment.delete()
        return redirect(post.get_absolute_url())
    else:
        raise PermissionDenied


class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment  # 자동으로 댓글 수정 폼에 내용 채워라?
    form_class = CommentForm

    # comment_form.html -> 이걸 자동으로 찾음. 안 만들면, 못 찾는다고 에러 뜸!

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


# class PostList(ListView): model=Post(Post.objects.all) post는 모두 불러오는것 내포하고있음 => post_list.html
# def get_queryset(self):
#       post_list=Post.objects.all  이렇게됌.
class PostSearch(PostList):  # post_list.html
    paginated_by = None  # pagination 안하겠다

    def get_queryset(self):  # Post(Post.objects.all) 이게 불러와진다
        q = self.kwargs['q']
        post_list = Post.objects.filter(Q(title__contains=q) | Q(tags__name__contains=q)).distinct()
        return post_list

    def get_context_data(self, **kwargs):
        context = super(PostSearch, self).get_context_data()
        q = self.kwargs['q']
        context['search_info'] = f'Search:{q}({self.get_queryset().count()})'

        return context

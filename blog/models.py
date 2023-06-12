from django.db import models
from django.contrib.auth.models import User
import os

from django.shortcuts import render


# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)  # allow unicode= 한글도 가능하게
    def __str__(self):
        return self.name


class Category(models.Model):  # DB table
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(max_length=200, unique=True, allow_unicode=True)  # allow unicode= 한글도 가능하게

    # slug: 주요단어 뽑아내는 것.(제목화 될수 있는것들) html코드로만 쓸수 있는거만 가능

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/blog/category/{self.slug}'

    class Meta:
        verbose_name_plural = 'Categories'  # 테이블에 이름 강제 지정 가능함.


class Post(models.Model):
    title = models.CharField(max_length=30)
    hook_text = models.CharField(max_length=100, blank=True)
    content = models.TextField()
    head_image = models.ImageField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    # 이렇게 해야 서버에서 파일을 찾아오는 시간을 단축할 수 있음. blank=True <- 해당 필드는 필수 항목은 아니라는 뜻
    file_upload = models.FileField(upload_to='blog/images/%Y/%m/%d/', blank=True)
    # head_image는 이미지, file_upload는 파일을 가져오는 것.
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)  # 시간 자동으로 저장되게 하기.
    # author: 추후 작성 예정

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    # null=True -> null값이 들어가도 된다는 의미 / on_delete=SET_NULL은 삭제된 정보는 null로 처리함 이때 null=True로 되어있어야함
    # on_delete=models.CASCADE # 정보 싹다 삭제

    # category는 일대다 관계일때 사용했음
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.SET_NULL)

    # tag는 다대다 관계임. -> ForeignKey가 아니라 ManyToManyField로 해야함
    tags = models.ManyToManyField(Tag, blank=True)
    def __str__(self):
        return f'[{self.pk}]{self.title} :: {self.author}'

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'

    def get_file_name(self):
        return os.path.basename(self.file_upload.name)

    def get_file_ext(self):
        return self.get_file_name().split('.')[-1]  # -1은 마지막 인덱스 ex) txt / xlsx / docx


class Comment(models.Model):
    post=models.ForeignKey(Post,on_delete=models.CASCADE) # 혼자 해야돼서 일대다 관계여서 foreignkey로 함.
    author=models.ForeignKey(User,on_delete=models.CASCADE) # 혼자 해야돼서 일대다 관계여서 foreignkey로 함.
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.author}::{self.content}'

    def get_absolute_url(self):
        return f'{self.post.get_absolute_url()}#comment-{self.pk}' # 현재글 이므로 해당 페이지+ #(anchor)id 이다.
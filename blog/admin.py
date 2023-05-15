from django.contrib import admin

# Register your models here.

from .models import Post,Category,Tag
admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)} # 자동으로 채워주는 역할을 하는 field

admin.site.register(Category,CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)}

admin.site.register(Tag,TagAdmin)


# 전체 테스트 = python manage.py test
# 특정 테스트= python manage.py test 파일명 ex) blog.test2category
# 테스트 코드 수정하지말고 테스트 할 것.


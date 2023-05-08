from django.contrib import admin

# Register your models here.

from .models import Post,Category
admin.site.register(Post)

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',)} # 자동으로 채워주는 역할을 하는 field

admin.site.register(Category,CategoryAdmin)
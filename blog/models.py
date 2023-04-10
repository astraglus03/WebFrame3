from django.db import models

# Create your models here.

class Post(models.Model): # 일종의 DB구조, field 설정하는 부분
    title=models.CharField(max_length=30)
    content=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    #author

    def __str__(this):
        return f'[{this.pk}]{this.title}' # 이게f'' 장고에서 문자열임.

    def get_absolute_url(self):
        return f'/blog/{self.pk}/'


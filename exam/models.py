from django.db import models


# Create your models here.

class Student(models.Model):
    num = models.CharField(max_length=15)
    name = models.CharField(max_length=50)
    birth = models.DateField()
    depart = models.CharField(max_length=100)
    image = models.ImageField(upload_to='exam/images/%Y/%m/%d/', blank=True)

    def __str__(self):
        return f'[{self.num}]{self.name}'

    def get_absolute_url(self):
        return f'/exam/prob/{self.pk}/'

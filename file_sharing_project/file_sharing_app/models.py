import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings


class MyUser(AbstractUser):
    first_name = models.CharField(max_length=30)
    is_ops_user = models.BooleanField(default=False)  
    def __str__(self):
        return self.username


    
class File(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255,default='File_Name')
    file = models.FileField(upload_to='files/')
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.file.name

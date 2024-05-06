from django.db import models


# Create your models here.
class UserInfo(models.Model):
	name = models.CharField(verbose_name="姓名", max_length=20)  # varchar
	age = models.IntegerField(verbose_name="年龄")  # int
	email = models.EmailField(verbose_name="Email", max_length=32)  # varchar

from django.db import models
from accounts.models import User
from django.conf import settings
from django.contrib.auth import get_user_model

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()

    # 1. 직접참조 => 선호하지 않음
    # user = models.ForeignKey(User, on_delete=models.CASCADE) # 누구와 연결할지
    # 2. settings.py 변수 활용
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    # 3. get_user_model() 함수 실행
    # user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
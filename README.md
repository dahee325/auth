- User, Post, Comment


# 00. setting
- `python -m venv venv`
- `source venv/Scripts/activate`
- `pip install django`
- `.gitignore` 설정 : python, windeows, macOS, django


# 01. project
- `django-admin startproject auth .`
- `django-admin startapp accounts` : User
- `auth/settings.py` : `accounts`앱 등록


# 02. 공통 base.html 설정
- `AUTH/templates/base.html` : 폴더랑 파일 생성
- `auth/settings.py`에 `templates` 등록
- `templates/base.html`
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-QWTKZyjpPEjISv5WaRU9OFeRpok6YctnYmDr5pNlyT2bRjXh0JMhjY6hW+ALEwIH" crossorigin="anonymous">
</head>
<body>
    <div class="container">
        {% block body %}
        {% endblock %}
    </div>
    <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js" integrity="sha384-YvpcrYf0tY3lHB60NNkmXc5s9fDVZLESaAA55NDzOxhy9GkcIdslK1eN7N6jIeHz" crossorigin="anonymous"></script>
</body>
</html>
```

# 03. [User](https://docs.djangoproject.com/en/5.1/topics/auth/customizing/)
## 3-1. Modeling
- `accounts/models.py` : 장고가 미리 만들어놓은 앱스트립트 사용\
=> 변수를 추가하고싶으면 `User`클래스 안에 선언
```python
from django.db import models
from django.contrib.auth.models import AbstractUser

# 변수가 추가되는 등 나중에 확장될 경우를 대비해 미리 모델 확장
class User(AbstractUser): 
    pass 
    # phone = models.~~ # 나중에 model에 추가하기만 하면 됨
```
- `auth/settings.py` : 장고가 만든 관리자 창의 User말고 내가 만든 User 사용할 것이라고 알려줌
```python
...
AUTH_USER_MODEL = 'accounts.User' # 대소문자 주의
```

## 3-2. Migratioin
- `python manage.py makemigrations`
- `python manage.py migrate`

## 3-3. 로그인 기능 만들기 (Create)
- `auth/urls.py` : 경로 설정
```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls'))
]
```
- `accounts/urls.py` 파일 생성
```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup')
]
```
- `accounts/views.py`
```python
from django.shortcuts import render

# Create your views here.
def signup(request):
    if request.method == 'POST':
        pass
    else:
        form = UserForm()
```
- `accounts/forms.py` 파일 생성 => 장고가 만들어놓은 form 그대로 사용
```python
from .models import User
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = User 
        # 장고가 만들어놓은 UserCreationForm에서 model만 우리가 만든 USer로 바꿈
        fields = '__all__'
```
- `accounts/views.py`
```python
from django.shortcuts import render
from .forms import CustomUserCreationForm

# Create your views here.
def signup(request):
    if request.method == 'POST':
        pass
    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)
```
- `accounts/templates/signup.html`
```html
{% extends 'base.html' %}

{% block body %}
    {{form}}

{% endblock %}
```
- `accounts/forms.py`
```python
class CustomUserCreationForm(UserCreationForm):
    class Meta():
        model = User 
        # 장고가 만들어놓은 UserCreationForm에서 model만 우리가 만든 USer로 바꿈
        # fields = '__all__'
        fields = ('username', )
```
- `accounts/templates/signup.html`
```html
{% extends 'base.html' %}

{% block body %}
<form action="" method="POST">
    {% csrf_token %}
    {{form}}
    <input type="submit">
</form>
{% endblock %}
```
- `accounts/views.py` : if문 채우기(저장)
```python
from django.shortcuts import render, redirect

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')

    else:
        ...
```

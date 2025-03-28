- User, Article, Comment


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

## 3-3. Signup 기능 만들기 (Create)
- `auth/urls.py` : 경로 설정
```python
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
]
```
- `accounts/urls.py` 파일 생성
```python
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
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
    ### Hash
    - **해시 함수(hash function)** : 임의의 길이를 가진 데이터를 입력받아 고정된 길이의 값, 즉 해시값을 출력하는 함수
    - [SHA1 HASH](http://www.sha1-online.com/)
    - rainbow table : 모든 해시의 경우의수를 모아놓은 테이블
    - 비밀번호를 해시함수로 바꾸면 해시를 비밀번호로 바꿀 수 없음 => 해시함수 경우의 수를 하나하나 해보면서 비밀번호를 찾아봐야함


## 3-4. Login 기능 만들기 (Create)
- 내 데이터를 주고 전체 데이터를 받음
- `accounts/urls.py` : 경로 설정
```python
app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'), 
]
```
    ### 개발자도구 Cookies
    -  웹사이트 개발자도구의 `Application/Storage/Cookies` : 인터넷(크롬, 엣지)안의 행동(정보)에 대해서 저장(기록) => ex.장바구니, 로그인
    - 아이디의 비밀번호를 만들면 장고가 `user_session`에 로그인 상태를 암호화해서 저장함 => 그 암호화된 `session`을 갖고있으면 로그인한 상태가 됨
        - `expire_date` : `session`의 만료기간 => ex. 자동로그인을 해놨을 때 `expire_date`가 2주면 2주동안 로그인 상태가 유지됨
    - '쿠키를 허용하시겠습니까?' : '정보를 사용해도 괜찮을까요??'를 의미함
        - 사이트의 팝업창 (닫기, 오늘 그만 보기) -> 오늘 그만 보기를 누르면 `Cookies/closePopup`이 `done`으로 돼서 새로고침하면 팝업창이 보이지 않음
        - `github`사이트의 로그인한 상태에서 개발자도구의 `Cookies/user_session`을 지우면 로그아웃된 상태가 됨

- `accounts/views.py`
```python
def login(request):
    if request.method == 'POST':
        pass
    else:
        pass
```
- `account/forms.py` : 장고가 만들어놓은 폼 확장
```python
class CustomAuthenticationForm(AuthenticationForm):
    pass
```
- `accounts/views.py`
```python
from .forms import CustomUserCreationForm, CustomAuthenticationForm

def login(request):
    if request.method == 'POST':
        pass
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)
```
- `accounts/templates/login.html` 파일 생성 : 로그인 창 보여주기
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
- `accounts/views.py`
```python
from django.contrib.auth import login as auth_login # 로그인을 처리해주는 함수
# 우리도 login함수를 만들었으므로 겹치지 않기 위해 장고의 login함수를 auth_login으로 불러옴

def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST) # user 정보 담기
        if form.is_valid():
            # user정보를 담았기 때문에 바로 저장하지 않음
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        ...
```

## 3-5. 링크 달기
- `templates/base.html`
```html
<body>
    <nav class="nav">
        <a href="" class="nav-link disabled">{{user}}</a>
        <!--context에 user를 넣지 않아도 user는 기본적으로 사용할 수 있음-->
        <a href="{% url 'accounts:signup' %}" class="nav-link">signup</a>
        <a href="(% url 'accounts:login' %)" class="nav-link">login</a>
        <a href="{% url 'accounts:logout' %}" class="nav-link">logout</a>
    </nav>
    <div class="container">
        {% block body %}
        {% endblock %}
    </div>
```

## 3-4. Logout 기능 만들기
- `accounts/urls.py`
```python
urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'), 
    path('logout/', views.logout, name='logout',),
]
```
- `accounts/views.py`
```python
from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)

    return redirect('accounts:login')
```

## 3-5. 로그인 상태에 따른 navbar 구조 변경
- `templates/base.html`
```html
<body>
    <nav class="nav">
        {% if user.is_authenticated %} <!--is_authenticated : 인증됐니?-->
            <a href="" class="nav-link disabled">{{user}}</a>
            <a href="{% url 'accounts:logout' %}" class="nav-link">logout</a>

        {% else %}
            <a href="{% url 'accounts:signup' %}" class="nav-link">signup</a>
            <a href="{% url 'accounts:login' %}" class="nav-link">login</a>

        {% endif %}
    
    </nav>
    ...
</body>
```

# 04. Article
## 4-1. articles 앱 만들기
- `django-admin startapp articles`
- `auth/settings.py`에 앱 등록

## 4-2. Modeling
- `articles/models.py`
```python
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
```

## 4-3. Migration
- `python manage.py makemigrations`
- `python manage.py migrate`

## 4-4. Article
- `auth/urls.py`
```python
urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('articles/', include('articles.urls')),
]
```
- `articles/urls.py` 파일 생성
```python
from django.urls import path
from . import views

app_name = 'articles'

urlpatterns = [
    path('', views.index, name='index'), 
]
```
- `articles/views.py`
```python
def index(request):
    return render(request, 'index.html')
```
- `articles/templates/index.html` 폴더랑 파일 생성
```html
{% extends 'base.html' %}

{% block body %}
    <h1>index</h1>
{% endblock %}
```

## 4-5. Article Create
- `templates/base.html`
```html
<body>
    <nav class="nav">
        {% if user.is_authenticated %} <!--is_authenticated : 인증됐니?-->
            <a href="" class="nav-link disabled">{{user}}</a>
            <a href="{% url 'articles:create' %}" class="nav-link">create</a>
            <a href="{% url 'accounts:logout' %}" class="nav-link">logout</a>

        {% else %}
            ...

        {% endif %}
    
    </nav>
    ...
</body>
```
- `articles/urls.py`
```python
urlpatterns = [
    path('', views.index, name='index'), 
    path('create/', views.create, name='create'),
]
```
- `articles/views.py`
```python
def create(request):
    if request.method == 'POST':
        pass
    else:
        pass
```
- `articles/forms.py` 파일 생성
```python
from django.forms import ModelForm
from .models import Article

class ArticleForm(ModelForm):
    class Meta():
        model = Article
        fields = '__all__'
```
- `articles/views.py`
```python
from .forms import ArticleForm

def create(request):
    if request.method == 'POST':
        pass
    else:
        form = ArticleForm()
    
    context = {
        'form': form,
    }
    return render(request, 'create.html', context)
```
- `articles/templates/create.html` 파일 생성
```html
{% extends 'base.html' %}

{% block body %}
    <form action="" method="POST">
        {% csrf_token%}
        {{form}}
        <input type="submit" class="mt-3">
    </form>
{% endblock %}
```
- `articles/forms.py` : user 보이지 않게 설정
```python
class ArticleForm(ModelForm):
    class Meta():
        model = Article
        # fields = '__all__'
        
        # fields = ('title', 'content', )
        exclude = ('user', )
```
- `articles/views.py` : if문 채우기
```python
from django.shortcuts import render, redirect

def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False) # 임시저장, user정보가 없음(title, content만 있음)
            article.user = request.user # request.user에는 로그인한 사람의 정보가 들어있음
            article.save()
            return redirect('articles:index')
    else:
        ...
```

## 4-6. Article Read
- `articles/views.py`
```python
from .models import Article

def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'index.html', context)
```
- `articles/templates/index.html`
```html
{% block body %}
    <h1>index</h1>

    {% for article in articles %}
        <h3>{{article.title}}</h3>
        <p>{{article.content}}</p>
        <p>{{article.user}}</p>
        <hr>
    {% endfor %}
{% endblock %}
```

## 4-7. 로그인 상태에 따른 게시물 작성
- `articles/views.py`
```python
from django.contrib.auth.decorators import login_required
# decorators : 함수가 실행되기 전에 먼저 실행라하는 의미
# login_required : 로그인이 되어있으면 진행, 안되어있으면 진행x

@login_required
def create(request):
    ...
```

### accounts/login 경로 다시 설정
- `accounts/views.py`
```python
def login(request):
    if request.method == 'POST':
        ...
        if form.is_valid():
            # user정보를 담았기 때문에 바로 저장하지 않음
            auth_login(request, form.get_user())
            return redirect('articles:index')
    else:
        ...
```

## 4-8. next 인자 처리
- `accounts/views.py`
```python
def login(request):
    if request.method == 'POST':
        ...
        if form.is_valid():
            # user정보를 담았기 때문에 바로 저장하지 않음
            auth_login(request, form.get_user())

            # /accounts/login/
            # /accounts/login/?next=/articles/create
            next_url = request.GET.get('next') # get() : 있으면 next인자 반환, 없으면 none

            # next가 없을 때 => none or 'articles:index'
            # next가 있을 때 => 'articles/create' or 'articles:index'
            return redirect(next_url or 'articles:index')
    else:
        ...
```
## 4-9. detail, update, delete

## 4-10. bootstrap


# 05. Comment
## 5-1. modeling
- `articles/models.py`
```python
class Comment(models.Model):
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    article = models.ForeignKey(Article,on_delete=models.CASCADE)
```

## 5-2. Migration
- `python manage.py makemigrations`
- `python manage.py migrate`

## 5-3. 댓글 빈종이 보여주기
- `articles/forms.py`
```python
class CommentForm(ModelForm):
    class Meta():
        model = Comment
        fields = ('content', )
```
- `articles/views.py`
```python
def detail(request, id):
    article = Article.objects.get(id=id)
    form = CommentForm()
    context = {
        'article': article,
        'form': form, 
    }
    return render(request, 'detail.html', context)
```
- `articles/templates/detail.html`
```html
{% block body %}
    ...
    <form action="{% url 'articles:comment_create' article.id %}" method="POST">
        {% csrf_token%}
        {{form}}
        <input type="submit" value="댓글달기">
    </form>
    
{% endblock %}
```
## 5-4. Comment_Create
- `articles/urls.py`
```python
urlpatterns = [
    ...

    path('<int:article_id>/comments/create/', views.comment_create, name='comment_create'),
]
```
- `articles/views.py`
```python
@login_required
def comment_create(request, article_id):
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        
        # 객체를 저장하는 경우
        # comment.user = request.user
        # article = Article.objects.get(id=article_id)
        # comment.article = article

        # id값을 저장하는 경우 => article을 찾는 행위가 줄어듦
        comment.user_id = request.user.id
        comment.article_id = article_id

        comment.save()

        return redirect('article:detail', id=article_id)
```

## 5-5. Comment Read
- `araticles/templates/detail.html`
```html
{% block body %}
    ...
    {% for comment in article.comment_set.all %}
        <li class="card card-body">{{comment.user.username}} - {{comment.content}}</li>
    {% endfor %}

{% endblock %}
```

## 5-6. Comment Delete
- `articles/templates/detail.html`
```html
{% block body %}
    ...
    {% for comment in article.comment_set.all %}
        <li class="card card-body">{{comment.user.username}} - {{comment.content}}</li>
        <a href="{% url 'articles:comment_delete' article.id comment.id %}">delete</a>
    {% endfor %}

{% endblock %}
```
- `articles/urls.py`
```python
urlpatterns = [
    ...

    path('<int:article_id>/comments/create/', views.comment_create, name='comment_create'),
    path('<int:article_id>/comments/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),
]
```
- `articles/views.py`
```python
from .models import Article, Comment

def comment_delete(request, article_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    comment.delete()

    return redirect('articles:detail', id=article_id)
```

## 06. 특정 조건 설정
### 로그인한 사람과 댓글 작성자가 같을 경우 댓글 삭제
- `articles/templates/detail.html`
```html
{% block body %}
    ...
    {% for comment in article.comment_set.all %}
        <li class="card card-body">{{comment.user.username}} - {{comment.content}}</li>
        {% if user == comment.user %}
            <a href="{% url 'articles:comment_delete' article.id comment.id %}" class="btn btn-primary">delete</a>
        {% endif %}
    {% endfor %}

{% endblock %}
```
- `articles/views.py`
```python
@ login_required
def comment_delete(request, article_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.user:
        comment.delete()

    return redirect('articles:detail', id=article_id)
```

### 로그인한 사람과 게시글 작성자가 같을 경우 수정/삭제
- `articles/templates/detail.html`
```html
{% block body %}
    ...
    {% if user == article.user %}
    <a href="{% url 'articles:update' article.id %}" class="btn btn-warning mt-3">update</a>
    <a href="{% url 'articles:delete' article.id %}" class="btn btn-danger mt-3">delete</a>
    {% endif %}
    ...
{% endblock %}
```
- `articles/views.py`\
=> `if request.user != article.user:` 작성자가 아닌 사람이 URL주소로 접근하는 경우 제한 
```python
@login_required
def update(request, id):
    article = Article.objects.get(id=id)
    if request.user != article.user:
        return redirect('articles:index')

    if request.method == 'POST':
        form = ArticleForm(request.POST, instance=article)
        if form.is_valid():
            form.save()
            return redirect('articles:detail', id=id)
    else:
        form = ArticleForm(instance=article)
    context = {
        'form': form,
    }
    return render(request, 'update.html', context)

@login_required
def delete(request, id):
    article = Article.objects.get(id=id)
    if request.user == article.user:
        article.delete()

    return redirect('articles:index')
```
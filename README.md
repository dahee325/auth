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
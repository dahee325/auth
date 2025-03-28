from django.shortcuts import render, redirect
from .forms import ArticleForm, CommentForm
from .models import Article, Comment
from django.contrib.auth.decorators import login_required

# Create your views here.
def index(request):
    articles = Article.objects.all()
    context = {
        'articles': articles,
    }
    return render(request, 'index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False) # 임시저장, user정보가 없음(title, content만 있음)
            article.user = request.user # request.user에는 로그인한 사람의 정보가 들어있음
            article.save()
            return redirect('articles:index')
    else:
        form = ArticleForm()
    
    context = {
        'form': form,
    }
    return render(request, 'create.html', context)


def detail(request, id):
    article = Article.objects.get(id=id)
    form = CommentForm()
    context = {
        'article': article,
        'form': form, 
    }
    return render(request, 'detail.html', context)


def update(request, id):
    article = Article.objects.get(id=id)
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


def delete(request, id):
    article = Article.objects.get(id=id)
    article.delete()
    return redirect('articles:index')

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

        return redirect('articles:detail', id=article_id)

@ login_required
def comment_delete(request, article_id, comment_id):
    comment = Comment.objects.get(id=comment_id)
    if request.user == comment.user:
        comment.delete()

    return redirect('articles:detail', id=article_id)
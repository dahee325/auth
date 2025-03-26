from django.shortcuts import render, redirect
from .forms import ArticleForm

# Create your views here.
def index(request):
    return render(request, 'index.html')


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
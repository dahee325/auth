from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm, CustomAuthenticationForm
from django.contrib.auth import login as auth_login # 로그인을 처리해주는 함수
# 우리도 login함수를 만들었으므로 겹치지 않기 위해 장고의 login함수를 auth_login으로 불러옴
from django.contrib.auth import logout as auth_logout

# Create your views here.
def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')

    else:
        form = CustomUserCreationForm()

    context = {
        'form': form,
    }
    return render(request, 'signup.html', context)


def login(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, request.POST) # user 정보 담기
        if form.is_valid():
            # user정보를 담았기 때문에 바로 저장하지 않음
            auth_login(request, form.get_user())
            return redirect('accounts:login')
    else:
        form = CustomAuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'login.html', context)


def logout(request):
    auth_logout(request)

    return redirect('accounts:login')
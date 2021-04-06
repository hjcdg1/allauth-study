from django.conf import settings
from django.contrib.auth import logout as django_logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect


def home(request):
    return render(request, 'home.html')


def login(request):
    # 이미 로그인 된 상태라면 홈으로 리다이렉트
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        # TODO
        return redirect(request.POST['next'])

    context = {
        'next': request.GET.get('next', settings.LOGIN_REDIRECT_URL)
    }
    return render(request, 'login.html', context)


@login_required
def logout(request):
    django_logout(request)
    return redirect(request.META.get('HTTP_REFERER', './'))


def signup(request):
    # 이미 로그인 된 상태라면 홈으로 리다이렉트
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == 'POST':
        # TODO
        return redirect(request.POST['next'])

    context = {
        'next': request.GET.get('next', settings.LOGIN_REDIRECT_URL)
    }
    return render(request, 'signup.html', context)

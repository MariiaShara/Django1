from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from authapp.forms import MyAuthenticationForm, ShopUserRegisterForm, ShopUserProfileForm
from authapp.models import ShopUser


def login(request):
    next = request.GET['next'] if 'next' in request.GET.keys() else ''
    if request.method == 'POST':
        form = MyAuthenticationForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                if 'next' in request.POST.keys():
                    return HttpResponseRedirect(request.POST['next'])
                else:
                    return HttpResponseRedirect(reverse('main:index'))
    else:
        form = MyAuthenticationForm()

    context = {
        'page_title': 'logIn',
        'title': 'authentication',
        'a_btn_content': 'Sign up',
        'href': 'auth:user_register',
        'form': form,
        'next': next
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main:index'))


def user_register(request):
    if request.method == 'POST':
        form = ShopUserRegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.send_verify_mail()
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        form = ShopUserRegisterForm()

    context = {
        'page_title': 'Registration',
        'title': 'registration',
        'a_btn_content': 'Sign in',
        'href': 'auth:login',
        'form': form
    }
    return render(request, 'authapp/login.html', context)


def user_profile(request):
    if request.method == 'POST':
        form = ShopUserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('auth:user_profile'))
    else:
        form = ShopUserProfileForm(instance=request.user)

    context = {
        'page_title': 'Profile',
        'title': 'profile',
        'a_btn_content': 'Home',
        'href': 'main:index',
        'form': form
    }
    return render(request, 'authapp/profile.html', context)


def user_verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
        else:
            print(f'Error activation user: {user}')
        return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'Error activation user: {user}')
        return HttpResponseRedirect(reverse('main'))

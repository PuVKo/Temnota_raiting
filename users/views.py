from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm, UserUpdateForm, CustomPasswordChangeForm
from django.contrib.auth import logout
from django.contrib.auth import update_session_auth_hash

from verify_email.email_handler import send_verification_email


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            inactive_user = send_verification_email(request, form)
            messages.success(request, f'Подтвердите адрес электронной почты. Письмо уже направилось к вам!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def changepassword(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, f'Ваш пароль успешно изменён')
            return redirect('/profile')
        else:
            messages.success(request, f'Ошибка! Старый пароль введен неверно или новые пароли не совпадают!')
            return redirect('/changepassword')

    else:
        form = CustomPasswordChangeForm(user=request.user)
        return render(request, 'users/change_password.html', {'form': form})
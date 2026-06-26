from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages

def auth_view(request):
    login_form = AuthenticationForm()
    signup_form = UserCreationForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST:
            login_form = AuthenticationForm(data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                messages.success(request, "Tizimga muvaffaqiyatli kirdingiz!")
                return redirect('/')
            else:
                messages.error(request, "Login yoki parol xato.")

        elif 'signup_submit' in request.POST:
            signup_form = UserCreationForm(request.POST)
            if signup_form.is_valid():
                user = signup_form.save()
                login(request, user)
                messages.success(request, "Akkount muvaffaqiyatli yaratildi!")
                return redirect('/')
            else:
                messages.error(request, "Ro'yxatdan o'tishda xatolik yuz berdi.")

    context = {
        'login_form': login_form,
        'signup_form': signup_form
    }
    return render(request, 'accounts/auth.html', context)
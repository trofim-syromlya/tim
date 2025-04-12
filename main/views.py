from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import UserStatistics
from random import randint
from django.db import models


def index(request):
    return render(request, 'index.html', {'user': request.user})


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            return render(request, 'login.html', {
                'error_message': 'Это имя уже занято, пожалуйста, выберите другое.',
                'username': '',
                'password': ''
            })

        user = User.objects.create_user(username=username, password=password)
        UserStatistics.objects.create(user=user)

        success_message = ("Вы успешно зарегистрированы! Теперь вы можете авторизоваться.")
        return render(request, 'login.html', {
            'success_message': success_message,
            'username': '',
            'password': ''
        })

    return render(request, 'login.html', {
        'username': '',
        'password': ''
    })

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {
                'error_message': 'Такое имя не зарегистрировано, пожалуйста, зарегистрируйтесь!',
                'username': username,
                'password': password
            })

    return render(request, 'login.html', {
        'username': '',
        'password': ''
    })

def logout_view(request):
    logout(request)
    return redirect('index')

@login_required
def profile_view(request):
    return render(request, 'profile.html')

@login_required(login_url='/login/')
def amount(request):
    if 'num1' not in request.session or 'num2' not in request.session:
        request.session['num1'] = randint(1, 10)
        request.session['num2'] = randint(1, 10)

    num1 = request.session['num1']
    num2 = request.session['num2']

    correct_answer = num1 + num2

    if request.method == 'POST':
        answer = int(request.POST['answer'])

        if answer == correct_answer:
            UserStatistics.objects.filter(user=request.user).update(correct_answers=models.F('correct_answers') + 1)
            result = ('/ зачтено (ответ верный)')
            answered = True

            request.session['num1'] = randint(1, 10)
            request.session['num2'] = randint(1, 10)
        else:
            UserStatistics.objects.filter(user=request.user).update(incorrect_answers=models.F('incorrect_answers') + 1)
            result = ('/ не зачтено (ответ неверный, попробуйте еще...)')
            answered = False

    else:
        answered = False

    return render(request, 'amount.html', {
        'num1': num1,
        'num2': num2,
        'result': result if 'result' in locals() else None,
        'answered': answered
    })

@login_required(login_url='/login/')
def statistics(request):
    total_users = User.objects.count()

    try:
        user_stats = UserStatistics.objects.get(user=request.user)
    except UserStatistics.DoesNotExist:
        user_stats = UserStatistics.objects.create(user=request.user)

    correct_answers = UserStatistics.objects.aggregate(total=models.Sum('correct_answers'))['total'] or 0
    incorrect_answers = UserStatistics.objects.aggregate(total=models.Sum('incorrect_answers'))['total'] or 0

    user_total_attempts = user_stats.correct_answers + user_stats.incorrect_answers
    user_correct_percentage = round((user_stats.correct_answers / user_total_attempts) * 100) if user_total_attempts > 0 else 0
    user_incorrect_percentage = round((user_stats.incorrect_answers / user_total_attempts) * 100) if user_total_attempts > 0 else 0

    total_attempts = correct_answers + incorrect_answers
    correct_percentage = round((correct_answers / total_attempts) * 100) if total_attempts > 0 else 0
    incorrect_percentage = round((incorrect_answers / total_attempts) * 100) if total_attempts > 0 else 0

    context = {
        'total_users': total_users,
        'correct_answers': correct_answers,
        'incorrect_answers': incorrect_answers,
        'correct_percentage': correct_percentage,
        'incorrect_percentage': incorrect_percentage,
        'user_stats': user_stats,
        'user_correct_percentage': user_correct_percentage,
        'user_incorrect_percentage': user_incorrect_percentage
    }

    return render(request, 'statistics.html', context)

def about(request):
    return render(request, 'about.html')

def next_task(request):
    return redirect('amount')

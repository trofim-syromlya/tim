from .views import profile_view, index, amount, statistics, about, register, logout_view, next_task, login_view
from django.contrib.auth.views import LoginView
from django.urls import path

urlpatterns = [
    path('', index, name='index'),
    path('amount/', amount, name='amount'),
    path('statistics/', statistics, name='statistics'),
    path('about/', about, name='about'),
    path('register/', register, name='register'),
    path('logout/', logout_view, name='logout'),
    path('next_task/', next_task, name='next_task'),
    path('login/', login_view, name='login'),
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('accounts/profile/', profile_view, name='profile'),
]

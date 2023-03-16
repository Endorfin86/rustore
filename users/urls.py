from django.urls import path
from . import views
from django.contrib.auth import views as loginViews
from django.contrib.auth import views as logoutViews

urlpatterns = [
    path('registration', views.registration, name='registration'),
    path('login', loginViews.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout', logoutViews.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
]
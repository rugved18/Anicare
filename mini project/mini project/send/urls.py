from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('user/', views.user_page, name='user_page'),
    path('admin/', views.admin_page, name='admin_page'),
    path('redirectToUser/', views.redirectToUser, name='redirectToUser'),
    path('redirectToAdmin/', views.redirectToAdmin, name='redirectToAdmin'),
    path('redirectToLogin/', views.UserLogin, name='redirectToLogin'),
    path('Login/', views.UserLogin, name='UserLogin'),
    path('UserRegister/', views.UserRegister, name='UserRegister'),
    path('NgoLink/', views.NgoLink, name='NgoLink'),
    path('SubmitNgoForm/', views.SubmitNgoForm, name='SubmitNgoForm'),
    path('LoadEcommerce/', views.LoadEcommerce, name='LoadEcommerce'),
    path('redirectToServices/', views.redirectToServices, name='redirectToServices'),
]

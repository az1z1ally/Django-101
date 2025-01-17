from django.urls import path
from . import views

urlpatterns = [
  path('', views.profiles, name='profiles'),
  path('profile/<str:pk>/', views.userProfile, name='user-profile'),

  path('login/', views.loginPage, name='login'),
  path('register/', views.registerPage, name='register'),
  path('reset-password/', views.resetPasswd, name='reset-password'),
  path('logout/', views.logoutPage, name='logout'),
]
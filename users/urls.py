from django.urls import path
from . import views

urlpatterns = [
  path('', views.profiles, name='profiles'),
  path('profile/<str:pk>/', views.userProfile, name='user-profile'),

  path('login/', views.loginUser, name='login'),
  path('register/', views.registerPage, name='register'),
  path('reset-password/', views.resetPassword, name='reset-password'),
  path('change-password/', views.changePassword, name='change-password'),
  path('logout/', views.logoutUser, name='logout'),
]
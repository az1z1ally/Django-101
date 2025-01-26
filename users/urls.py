from django.urls import path
from . import views

urlpatterns = [
  path('', views.profiles, name='profiles'),
  path('profile/<str:pk>/', views.userProfile, name='user-profile'),
  path('account/', views.userAccount, name='account'),
  path('account/edit-account/', views.editAccount, name='edit-account'),

  path('account/login/', views.loginUser, name='login'),
  path('account/register/', views.registerPage, name='register'),
  path('account/reset-password/', views.resetPassword, name='reset-password'),
  path('account/change-password/', views.changePassword, name='change-password'),
  path('account/logout/', views.logoutUser, name='logout'),

  # skills
  path('skill/create-skill/', views.createSkill, name='create-skill'),
  path('skill/edit-skill/<str:pk>/', views.editSkill, name='edit-skill'),
  path('skill/delete-skill/<str:pk>/', views.deleteSkill, name='delete-skill'),
]
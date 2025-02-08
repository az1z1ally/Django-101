from django.urls import path
from . import views

urlpatterns = [
  path('', views.inbox, name='inbox'),
  path('message/<str:message_id>/', views.viewMessage, name='message'),
  path('send-message/<str:recipient_id>/', views.sendMessage, name='send-message'),
]
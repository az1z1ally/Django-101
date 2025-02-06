from django.urls import path
from . import views

urlpatterns = [
  path('', views.projects, name='projects'),
  path('project-detail/<str:pk>/', views.projectDetail, name='project'),
  path('project-detail/<str:pk>/<str:review_id>/', views.projectDetail, name='project-review-id'),

  path('create-project/', views.createProject, name='create-project'),
  path('update-project/<str:pk>/', views.updateProject, name='update-project'),
  path('delete-project/<str:pk>/', views.deleteProject, name='delete-project'),

  # Project reviews
  path('add-project-review/<str:project_id>/', views.addProjectReview, name='add-project-review'),
  path('edit-project-review/<str:review_id>/', views.editProjectReview, name='edit-project-review'),
  path('delete-project-review/<str:review_id>/', views.deleteProjectReview, name='delete-project-review'),
]
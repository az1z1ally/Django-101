from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from .models import Project

def user_is_project_owner(function):
  def wrap(request, *args, **kwargs):
    project = get_object_or_404(Project, pk=kwargs['pk'])
    if project.owner != request.user.profile:
      # return HttpResponseForbidden()
      return HttpResponseForbidden("You are not allowed to edit this project.")
    return function(request, *args, **kwargs)
  return wrap

from django.shortcuts import render
from .models import Project

# Create your views here.
def projects(request):
  projectList = Project.objects.all()
  context = {'projects': projectList}
  return render(request, 'projects/projects.html', context)

def project(request, pk):
  projectObj = Project.objects.get(id=pk)
  context = {'project': projectObj}
  return render(request, 'projects/single-project.html', context)
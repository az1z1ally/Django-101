from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .forms import ProjectForm
from .models import Project

# Create your views here.
def projects(request):
  projectList = Project.objects.all()
  context = {'projects': projectList}
  return render(request, 'projects/projects.html', context)


def project(request, pk):
  projectObj = Project.objects.get(id=pk)
  context = {'project': projectObj}
  return render(request, 'projects/single_project.html', context)

@login_required(login_url='login')
def createProject(request):
  profile = request.user.profile
  form = ProjectForm()
  next_url = request.GET.get('next', 'projects')

  if request.method == 'POST':
    form = ProjectForm(request.POST, request.FILES)
    if form.is_valid():
      project = form.save(commit=False)
      project.owner = profile
      project.save()
      return redirect(next_url)

  context = {'form': form}
  return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def updateProject(request, pk):
  profile = request.user.profile
  next_url = request.GET.get('next', 'projects')
  try:
    project = profile.projects.get(id=pk) # Prevent user from editing other users projects
  except:
    return redirect(next_url)
  form = ProjectForm(instance=project)

  if request.method == 'POST':
    form = ProjectForm(request.POST, request.FILES, instance=project)
    if form.is_valid():
      form.save()
      return redirect(next_url)

  context = {'form': form}
  return render(request, 'projects/project_form.html', context)


@login_required(login_url='login')
def deleteProject(request, pk):
  profile = request.user.profile
  next_url = request.GET.get('next', 'projects')
  try:
    project = profile.projects.get(id=pk) # Prevent user from deleting other users projects
  except:
    return redirect(next_url)

  if request.method == 'POST':
    project.delete()
    return redirect(next_url)

  context = {'object': project}
  return render(request, 'delete_template.html', context)
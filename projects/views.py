from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from projects.filters import ProjectFilter, search_projects
from projects.paginations import paginateProjects
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from .forms import ProjectForm
from .models import Project

# Create your views here.
def projects(request):
  search_query, projects = search_projects(request)

   # Apply filter to the projects queryset
  filter = ProjectFilter(request.GET, queryset=projects)
  filtered_projects = filter.qs

  # Paginate the filtered queryset
  paginator, page_obj, custom_range = paginateProjects(request, filtered_projects, 10)

  context = {'paginator': paginator, 'page_obj': page_obj, 'custom_range': custom_range, 'projects': page_obj.object_list, 'search_query': search_query, 'filter': filter}
  return render(request, 'projects/projects.html', context)


def project(request, pk):
  try:
    projectObj = Project.objects.get(id=pk)
  except ObjectDoesNotExist:
    # Handle the case where the project does not exist
    return render(request, '404.html', status=404)
  except MultipleObjectsReturned:
    # Handle the case where multiple objects are returned
    return render(request, 'error.html')

  is_owner = request.user.profile == projectObj.owner and projectObj.owner is not None
  context = {'project': projectObj, 'is_owner': is_owner}

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
      messages.success(request, f'Project created successfully! 🤗✅')
      return redirect(next_url)
    
    else:
      messages.error(request, f'Failed to create the project! ⚡⚠️')

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
      messages.success(request, f'Project updated successfully! 🤗✅')
      return redirect(next_url)
    
    else:
      messages.error(request, f'Failed to update the project! ⚡⚠️')

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
    messages.success(request, f'Project removed successfully! 🤗✅')
    return redirect(next_url)

  context = {'object': project}
  return render(request, 'delete_template.html', context)
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from projects.filters import ProjectFilter, search_projects
from projects.paginations import paginateProjects
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from django.db import transaction

from .forms import ProjectForm, ReviewForm
from .models import Project, Review

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


def projectDetail(request, pk, review_id=None):
  try:
    project = Project.objects.get(id=pk)
  except ObjectDoesNotExist:
    # Handle the case where the project does not exist
    return render(request, '404.html', status=404)
  except MultipleObjectsReturned:
    # Handle the case where multiple objects are returned
    return render(request, 'error.html')

  # Handle pre-filled review form for editing
  if review_id:
    try:
      profile = request.user.profile
      review = profile.owner_reviews.get(id=review_id) # Prevent user from editing other users reviews
    except:
      return render(request, '404.html', status=404)
  else:
    review = None

  form = ReviewForm(instance=review)
  reviews_with_body = project.project_reviews.exclude(body__isnull=True).exclude(body__exact='').all() # Get all reviews where the body field is not empty

  context = {
    'project': project,
    'reviews_with_body': reviews_with_body,
    'form': form,
    'edit_mode': review is not None,
    'review_id': review.id if review else None
  }

  return render(request, 'projects/project_detail.html', context)


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
      messages.success(request, f'Project created successfully! 👍✅')
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
      messages.success(request, f'Project updated successfully! 👍✅')
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
    messages.success(request, f'Project removed successfully! 👍✅')
    return redirect(next_url)

  context = {'object': project}
  return render(request, 'delete_template.html', context)


# Project reviews CRUD
@login_required(login_url='login')
def addProjectReview(request, project_id):
  try:
    project = Project.objects.get(id=project_id)
  except ObjectDoesNotExist:
    # Handle the case where the project does not exist
    return render(request, '404.html', status=404)
  except MultipleObjectsReturned:
    # Handle the case where multiple objects are returned
    return render(request, 'error.html')

  if request.method == 'POST':
    profile = request.user.profile

    # Ensure user can not review their own project
    if profile and profile == project.owner:
      messages.error(request, 'You can not review your own project⚠️⚡')
      return redirect('project', pk=project.id)
    
    # Ensure user can not submit more than one review
    if profile.id in project.get_reviewers_ids:
      messages.error(request, 'You have already reviewed this project⚠️⚡')
      return redirect('project', pk=project.id)

    form = ReviewForm(request.POST)

    if form.is_valid():
      with transaction.atomic(): # ensure errors in signals operations(i.e. calculating votes_total & ratio) undo the entire db operations
        review = form.save(commit=False)
        review.project = project
        review.owner = profile
        review.save()

        messages.success(request, 'Review added successfully! 👍✅')
        return redirect('project', pk=project.id) # Redirect to the same page to clear the form
    else:
      messages.error(request, 'Failed to add a review ⚠️⚡')

  # If GET request or form is not valid, render the project detail page.
  return redirect('project', project.id)


@login_required(login_url='login')
def editProjectReview(request, review_id):
  profile = request.user.profile

  try:
    review = profile.owner_reviews.get(id=review_id)
  except ObjectDoesNotExist:
    # Handle the case where the project does not exist
    return render(request, '404.html', status=404)

  if request.method == 'POST':
    form = ReviewForm(request.POST, instance=review)

    if form.is_valid():
      with transaction.atomic(): # To ensure the entire project db operations(i.e. post_save signal) done or nothing is done
        form.save()
        messages.success(request, 'Review updated successfully. 👍✅')
        return redirect('project', pk=review.project.id)
    else:
      messages.error(request, 'Failed to update the review. ⚠️⚡')

  # If GET request or form is not valid, render the project detail page.
  return redirect('project', review.project.id)


@login_required(login_url='login')
def deleteProjectReview(request, review_id):
  profile = request.user.profile

  try:
    review = profile.owner_reviews.get(id=review_id)
  except ObjectDoesNotExist:
    # Handle the case where the project does not exist
    return render(request, '404.html', status=404)
  
  project_id = review.project.id

  if request.method == 'POST':
    with transaction.atomic(): # To ensure the entire project db operations(i.e. post-delete signal ) done or nothing is done
      review.delete()
      messages.success(request, 'Review deleted successfully. 👍✅')
      return redirect('project', pk=project_id)

  context = {'object': review}
  return render(request, 'delete_template.html', context)

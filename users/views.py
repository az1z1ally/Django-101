from django.db import transaction
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned

from shared.helpers.functions import get_redirect_url
from users.filters import ProfileFilter, search_profiles
from users.paginations import paginateProfiles
from .forms import CustomPasswordChangeForm, CustomUserCreationForm, ProfileForm, SkillForm
from .models import Profile

# Create your views here.
User = get_user_model()

def loginUser(request):
  if request.user.is_authenticated:
    return redirect(request.META.get('HTTP_REFERER', '/'))

  if request.method == 'POST':
    username = request.POST['username'].lower()
    password = request.POST['password']
    next_url = request.GET.get('next', '/') # Retrieve the 'next' parameter

    try:
      user_exists = User.objects.filter(username=username).exists() # Check if the user exist in the db
      if user_exists:
        user=authenticate(request, username=username, password=password)
        if user is not None:
          login(request, user) # Persist a user id and a backend in the request. This way a user doesn't have to reauthenticate on every request.
          # return redirect(request.GET['next'] if 'next' in request.GET else '/')
          return redirect(next_url) # Redirect to the 'next' URL or the default URL
          # messages.info(request, f'welcome back, {user.username} 🤗')
        else:
          messages.error(request, 'Username or password is incorrect! ⚠️⚡')
      else:
        messages.error(request, 'Username or password is incorrect! ⚠️⚡')

    except Exception as e:
      messages.error(request, 'Failed to authenticate the user! ⚠️⚡')

  context = {'page': 'login'}
  return render(request, 'users/login_register.html', context)


def registerPage(request):
  form = CustomUserCreationForm()

  if request.method == 'POST':
    form = CustomUserCreationForm(request.POST)
    if form.is_valid(): 
      try:
        # The transaction.atomic() block ensures that all operations within it are atomic—meaning they all succeed or none of them do(including the signal that creates the profile).
        with transaction.atomic():
          user = form.save(commit=False)
          user.username = user.username.lower()
          user.save() # This triggers the post_save signal that creates the profile(same when the user was created using create())
          messages.success(request, 'User Account was created successfully! 🤗✅')
          
          if user is not None:
              login(request, user) # Persist a user id and a backend in the request. This way a user doesn't have to reauthenticate on every request.
              # return redirect(reverse('profile', args=[user.profile.id])) # Generates the URL for the profile view with the specified profile_details_id, redirect() takes the generated URL and redirects the user to that URL.
              return redirect('edit-account')
          else:
            messages.error(request, 'Login failed! ⚠️⚡')

      except Exception as e:
        messages.error(request, f'An error has occurred during registration! ⚠️⚡: {str(e)}')

    else:
      messages.error(request, 'An error has occurred during registration! ⚠️⚡')

  context = {'page': 'register', 'form': form}
  return render(request, 'users/login_register.html', context)


def resetPassword(request):
  pass


@login_required(login_url='login')
def changePassword(request):
  current_user = request.user
  form = CustomPasswordChangeForm(current_user)
  next_url = request.GET.get('next', 'account')

  if request.method == 'POST':
    form = CustomPasswordChangeForm(current_user, request.POST)
    if form.is_valid():
      user = form.save()
      update_session_auth_hash(request, user)  # Important to update the session with the new password
      messages.success(request, 'Your password was successfully updated! 🤗✅')
      return redirect(next_url)
    
    else:
      messages.error(request, 'An error has occurred during password change, try again later! ⚠️⚡')
  
  context = {'form': form}
  return render(request, 'users/change_password.html', context)


@login_required(login_url='login')
def logoutUser(request):
  url_with_parameters = get_redirect_url(request, 'login')
  logout(request) # Remove the authenticated user's ID from the request and flush their session data
  messages.info(request, 'User was logged out successfully! 🤗')

  # Redirect to the URL with parameters
  return redirect(url_with_parameters)
  

def profiles(request):
  # Apply filter to profiles queryset
  search_query, profiles = search_profiles(request)
  filter = ProfileFilter(request.GET, queryset=profiles)
  filtered_profiles = filter.qs
  
  # Paginate the filtered queryset
  paginator, page_obj, custom_range = paginateProfiles(request, filtered_profiles, 10)

  context = {'paginator': paginator, 'page_obj': page_obj, 'custom_range': custom_range, 'profiles': page_obj.object_list, 'search_query': search_query, 'filter': filter}
  return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
  try:
    profile = Profile.objects.get(id=pk)
  except ObjectDoesNotExist:
    # Handle the case where the project does not exist
    return render(request, '404.html', status=404)
  except MultipleObjectsReturned:
    # Handle the case where multiple objects are returned
    return render(request, 'error.html')
  
  topSkills = profile.skill_set.exclude(description__exact='')
  otherSkills = profile.skill_set.filter(description='')
  projects_gt_5 = profile.projects.all().count() > 5
  projects = profile.projects.all()[:5]
  context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills, 'projects': projects, 'projects_gt_5': projects_gt_5}
  return render(request, 'users/profile_details.html', context)


@login_required(login_url='login')
def userAccount(request):
  profile = request.user.profile
  projects_gt_5 = profile.projects.all().count() > 5
  projects = profile.projects.all()[:5]  # Fetch only the first 5 projects
  context = {'profile': profile, 'projects': projects, 'projects_gt_5': projects_gt_5}
  return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
  profile = request.user.profile
  form = ProfileForm(instance=profile)

  if request.method == 'POST':
    form = ProfileForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
      with transaction.atomic(): # This ensures that if any failures happen then both the profile and the user update in the signal rolled-back
        form.save()
        messages.success(request, f'Account updated successfully! 🤗✅')
        return redirect('account')
    else:
      messages.error(request, f'Failed to update your account, try again! ⚡⚠️')
  
  context = {'form': form}
  return render(request, 'users/profile_form.html', context)


def deleteAccount(request):
  pass


# Skills CRUD
@login_required(login_url='login')
def createSkill(request):
  profile = request.user.profile
  next_url = request.GET.get('next', 'account')
  form = SkillForm()

  # Check if the user already has 10 skills
  if profile.skill_set.count() >= 10:
    messages.error(request, f'You have reached the maximum limit of 10 skills. 🎯❌')
    return redirect(next_url)

  if request.method == 'POST':
    form = SkillForm(request.POST)
    if form.is_valid():
      skill = form.save(commit=False)
      skill.owner = profile
      skill.save()
      messages.success(request, f'Skill added successfully! 🤗✅')
      return redirect(next_url)
    
    else:
      messages.error(request, f'Failed to add a skill, try again! ⚡⚠️')

  context = {'form': form}
  return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def editSkill(request, pk):
  profile = request.user.profile
  next_url = request.GET.get('next', 'account')
  try:
    skill = profile.skill_set.get(id=pk) # Prevent user from editing other users skills
  except:
    return redirect(next_url)
  
  form = SkillForm(instance=skill)

  if request.method == 'POST':
    form = SkillForm(request.POST, instance=skill)
    if form.is_valid():
      form.save()
      messages.success(request, f'Skill updated successfully! 🤗✅')
      return redirect(next_url)
    
    else:
      messages.error(request, f'Failed to update skill, try again! ⚡⚠️')

  context = {'form': form}
  return render(request, 'users/skill_form.html', context)


@login_required(login_url='login')
def deleteSkill(request, pk):
  owner = request.user.profile
  next_url = request.GET.get('next', 'account')
  try:
    skill = owner.skill_set.get(id=pk) # Prevent user from deleting other users skills
  except:
    return redirect(next_url)

  if request.POST:
    skill.delete()
    messages.success(request, f'Skill removed successfully! 🤗✅')
    return redirect(next_url)
  
  context = {'object': skill}
  return render(request, 'delete_template.html', context)
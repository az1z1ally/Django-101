from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.urls import reverse

from shared.helpers.functions import get_redirect_url
from .forms import CustomUserCreationForm, ProfileForm
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
      user = form.save(commit=False)
      user.username = user.username.lower()
      user.save()
      messages.success(request, 'User Account was created successfully! 🤗✅')
      
      if user is not None:
          login(request, user) # Persist a user id and a backend in the request. This way a user doesn't have to reauthenticate on every request.
          # return redirect(reverse('user-profile', args=[user.profile.id])) # Generates the URL for the profile view with the specified user_profile_id, redirect() takes the generated URL and redirects the user to that URL.
          return redirect('edit-account')
      else:
        messages.error(request, 'Login failed! ⚠️⚡')

    else:
      messages.error(request, 'An error has occurred during registration! ⚠️⚡')

  context = {'page': 'register', 'form': form}
  return render(request, 'users/login_register.html', context)


def resetPassword(request):
  pass


def changePassword(request):
  pass


@login_required(login_url='login')
def logoutUser(request):
  url_with_parameters = get_redirect_url(request, 'login')
  logout(request) # Remove the authenticated user's ID from the request and flush their session data
  messages.info(request, 'User was logged out successfully! 🤗')

  # Redirect to the URL with parameters
  return redirect(url_with_parameters)
  

def profiles(request):
  if request.user.is_authenticated:
    current_user = request.user
    profiles = Profile.objects.exclude(user=current_user)
  else:
    profiles = Profile.objects.all()

  context = {'profiles': profiles}
  return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
  profile = Profile.objects.get(id=pk)
  topSkills = profile.skill_set.exclude(description__exact='')
  otherSkills = profile.skill_set.filter(description='')
  context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
  return render(request, 'users/user_profile.html', context)


@login_required(login_url='login')
def userAccount(request):
  profile = request.user.profile
  projects = profile.projects.all()[:5]  # Fetch only the first 5 projects
  context = {'profile': profile, 'projects': projects}
  return render(request, 'users/account.html', context)


@login_required(login_url='login')
def editAccount(request):
  profile = request.user.profile
  form = ProfileForm(instance=profile)

  if request.method == 'POST':
    form = ProfileForm(request.POST, request.FILES, instance=profile)
    if form.is_valid():
      form.save()
      return redirect('account')
  
  context = {'form': form}
  return render(request, 'users/profile_form.html', context)
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required

from shared.helpers.functions import get_redirect_url
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
          # messages.info(request, f'welcome back, {user.username} 🤗')
          return redirect(next_url) # Redirect to the 'next' URL or the default URL
        else:
          messages.error(request, 'Username or password is incorrect! ⚠️⚡')
      else:
        messages.error(request, 'Username or password is incorrect! ⚠️⚡')

    except Exception as e:
      messages.error(request, 'Failed to authenticate the user! ⚠️⚡')

  context = {'page': 'login'}
  return render(request, 'users/login_register.html', context)


def registerPage(request):
  context = {'page': 'register'}
  return render(request, 'users/login_register.html', context)


def resetPassword(request):
  pass


def changePassword(request):
  pass


def logoutUser(request):
  url_with_parameters = get_redirect_url(request, 'login')
  if request.user.is_authenticated:
    logout(request) # Remove the authenticated user's ID from the request and flush their session data
    messages.info(request, 'User was logged out successfully! 🤗')

  # Redirect to the URL with parameters
  return redirect(url_with_parameters)
  

def profiles(request):
  profiles = Profile.objects.all()
  context = {'profiles': profiles}
  return render(request, 'users/profiles.html', context)


def userProfile(request, pk):
  profile = Profile.objects.get(id=pk)
  topSkills = profile.skill_set.exclude(description__exact='')
  otherSkills = profile.skill_set.filter(description='')
  context = {'profile': profile, 'topSkills': topSkills, 'otherSkills': otherSkills}
  return render(request, 'users/user-profile.html', context)
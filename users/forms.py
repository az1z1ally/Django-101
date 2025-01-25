from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
  class Meta:
    model = User
    fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']
    # labels = {
    #   'first_name': 'Name'
    # }

  # https://www.geeksforgeeks.org/how-to-add-html-attributes-to-input-fields-in-django-forms/
  def __init__(self, *args, **kwargs):
    super(CustomUserCreationForm, self).__init__(*args, **kwargs)

    for name, field in self.fields.items():
      field.widget.attrs.update({'class': 'input'})

    # self.fields['username'].widget.attrs.update({'class': 'input', 'placeholder': 'Enter ur username'})


class ProfileForm(ModelForm):
  class Meta:
    model = Profile
    fields = ['username', 'email', 'first_name', 'last_name', 'location', 'short_intro', 'bio', 'profile_image', 'social_github', 'social_x', 'social_linkedin', 'social_youtube', 'personal_website']
    labels = {
      'social_x': 'X Account',
      'social_github': 'Github Account',
      'social_linkedin': 'LinkedIn Account',
      'social_youtube': 'Youtube Account'
    }

  def __init__(self, *args, **kwargs):
    super(ProfileForm, self).__init__(*args, **kwargs)

    for name, field in self.fields.items():
      field.widget.attrs.update({'class': 'input'})
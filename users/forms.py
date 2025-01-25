from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
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
    self.fields['password2'].label = 'Confirm Password'

    for name, field in self.fields.items():
      field.widget.attrs.update({'class': 'input'})

    # self.fields['username'].widget.attrs.update({'class': 'input', 'placeholder': 'Enter ur username'})


class CustomPasswordChangeForm(PasswordChangeForm):
  class Meta:
    model = User
    fields = ('old_password', 'new_password1', 'new_password2')

  def __init__(self, *args, **kwargs):
    super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
    # sometimes the Meta class approach doesn't work as expected for built-in forms. Another way to update labels is to set them directly in the __init__ method:
    self.fields['old_password'].label = 'Your current password'
    self.fields['new_password1'].label = 'New password'
    self.fields['new_password2'].label = 'Confirm new password'
    
    for name, field in self.fields.items():
      field.widget.attrs.update({'class': 'input'})


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
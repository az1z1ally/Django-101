from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

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

    self.fields['username'].widget.attrs.update({'class': 'input', 'placeholder': 'Enter ur username'})
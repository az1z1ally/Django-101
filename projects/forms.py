from django import forms
from django.forms import ModelForm
from .models import Project

class ProjectForm(ModelForm):
   class Meta:
      model = Project
      fields = ['title', 'description', 'featured_image', 'demo_link', 'source_link', 'tags',] # fields = '__all__'

      widgets = {
         'tags': forms.CheckboxSelectMultiple()
      }

   # https://www.geeksforgeeks.org/how-to-add-html-attributes-to-input-fields-in-django-forms/
   def __init__(self, *args, **kwargs):
      super(ProjectForm, self).__init__(*args, **kwargs)

      for name, field in self.fields.items():
         field.widget.attrs.update({'class': 'input'})

      # self.fields['title'].widget.attrs.update({
      #    'class': 'input',
      #    'placeholder': 'Add Title'
      # })

      # self.fields['description'].widget.attrs.update({'class': 'input'})

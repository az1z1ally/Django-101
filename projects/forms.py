from django import forms
from django.forms import ModelForm
from .models import Project, Review

class ProjectForm(ModelForm):
   class Meta:
      model = Project
      fields = ('title', 'description', 'featured_image', 'demo_link', 'source_link', 'tags') # fields = '__all__'

      widgets = {
         'tags': forms.CheckboxSelectMultiple()
      }

   # https://www.geeksforgeeks.org/how-to-add-html-attributes-to-input-fields-in-django-forms/
   def __init__(self, *args, **kwargs):
      super(ProjectForm, self).__init__(*args, **kwargs)

      for name, field in self.fields.items():
         field.widget.attrs.update({'class': 'input'})

         if name == 'description':
            field.widget.attrs.update({'class': 'input input--textarea'})

      # self.fields['description'].widget.attrs.update({'class': 'input input--textarea'})


class ReviewForm(ModelForm):
   class Meta:
      model = Review
      fields = ['body', 'value']

      labels = {
         'body': 'Add a comment with your vote',
         'value': 'Place your vote',
      }

   def __init__(self, *args, **kwargs):
      super(ReviewForm, self).__init__(*args, **kwargs)

      for name, field in self.fields.items():
         field.widget.attrs.update({'class': 'input'})

         if name == 'value':
            field.widget.attrs.update({'class': 'input input--select'})
         
         if name =='body':
            field.widget.attrs.update({
               'class': 'input input--textarea',
               'placeholder': 'Write your comment ...'
            })
from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, arg):
  return field.as_widget(attrs={'class': arg})


@register.filter(name='add_placeholder')
def add_placeholder(field, arg):
  # modify the form field widget to include the specified placeholder text.
  return field.as_widget(attrs={'placeholder': arg})



# register = template.Library(): This creates a new template library where you can register your custom filters and tags.

# @register.filter(name='add_class'): This decorator registers the add_class function as a template filter named 'add_class'.

# def add_class(field, arg): This defines the add_class function which takes a form field (field) and a CSS class (arg) as arguments.

# return value.as_widget(attrs={'class': arg}): This modifies the form field widget to include the specified CSS class.
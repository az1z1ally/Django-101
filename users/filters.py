from django.http import HttpRequest
import django_filters
from .models import Profile, Skill
from django.db.models import Q


class SkillFilter(django_filters.FilterSet):
  name = django_filters.CharFilter(lookup_expr='icontains')

  class Meta:
    model = Skill
    fields = ['name']

class ProfileFilter(django_filters.FilterSet):
  username = django_filters.CharFilter(lookup_expr='icontains')
  short_intro = django_filters.CharFilter(lookup_expr='icontains')
  bio = django_filters.CharFilter(lookup_expr='icontains')
  first_name = django_filters.CharFilter(lookup_expr='icontains')
  last_name = django_filters.CharFilter(lookup_expr='icontains')
  skill__name = django_filters.CharFilter(lookup_expr='icontains')
  
  skills = django_filters.ModelMultipleChoiceFilter(
    field_name='skill__name',
    to_field_name='name',
    queryset=Skill.objects.all(),
    conjoined=True
  )

  class Meta:
    model = Profile
    fields = ['username', 'first_name', 'last_name', 'location', 'bio', 'short_intro', 'skills', 'skill__name']


'''Explanation:
  SkillFilter: Filters Skill model by name.

  ProfileFilter: Includes the Profile model filter fields plus a ModelMultipleChoiceFilter for skills.

  field_name='skill__name': Filters profiles by the name of the related skills.

  to_field_name='name': Ensures the filter works based on skill names.

  queryset=Skill.objects.all(): Uses all skills available.

  conjoined=True: Ensures that all selected skills must match.
'''
# Refer in doc.md file for more on django filters above


def search_profiles(request: HttpRequest):
  search_query = request.GET.get('search_query', '')

  # Logged in user should see only other profiles
  if request.user.is_authenticated:
    current_user = request.user
    profiles = Profile.objects.exclude(user=current_user)
  else:
    profiles = Profile.objects.all()

  if search_query:
    profiles = profiles.filter(
      Q(username__icontains=search_query) |
      Q(first_name__icontains=search_query) |
      Q(last_name__icontains=search_query) |
      Q(short_intro__icontains=search_query) |
      Q(bio__icontains=search_query) |
      Q(skill__name__icontains=search_query)
    ).distinct()
    '''
      Using distinct() is a common way to prevent duplicate results in Django queries. However, duplicates can occur without
      distinct() due to joins in the query. When you include related fields (like skill__name), it might result in multiple
      rows for a single profile, each representing a different skill. This multiplicity is where duplicates arise.
    '''

  return search_query, profiles

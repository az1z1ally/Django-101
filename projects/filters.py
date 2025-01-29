from django.http import HttpRequest
import django_filters
from .models import Project, Tag
from django.db.models import Q


class ProjectFilter(django_filters.FilterSet):
  title = django_filters.CharFilter(lookup_expr='icontains')
  desc = django_filters.CharFilter(lookup_expr='icontains')
  votes_ratio__gt = django_filters.NumberFilter(field_name='votes_ratio', lookup_expr='gt')
  votes_ratio__lt = django_filters.NumberFilter(field_name='votes_ratio', lookup_expr='lt')

  owner__username = django_filters.CharFilter(lookup_expr='iexact')
  owner__first_name = django_filters.CharFilter(lookup_expr='icontains')
  owner__last_name = django_filters.CharFilter(lookup_expr='icontains')
  description = django_filters.CharFilter(lookup_expr='icontains')

  class Meta:
    model = Project
    fields = ['title', 'owner', 'description', 'votes_ratio', 'votes_ratio__lt', 'votes_ratio__gt', 'owner__username', 'owner__first_name', 'owner__last_name']


def search_projects(request: HttpRequest):
  search_query = request.GET.get('search_query', '')
  projects= Project.objects.all()

  if search_query:
    tags = Tag.objects.filter(name__icontains=search_query)

    projects = projects.filter(
      Q(title__icontains=search_query) |
      Q(description__icontains=search_query) |
      Q(owner__username__icontains=search_query) |
      Q(owner__first_name__icontains=search_query) |
      Q(owner__last_name__icontains=search_query) |
      Q(tags__in=tags)
    ).distinct()

  return search_query, projects
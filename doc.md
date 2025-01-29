## DJANGO STATIC FILES

`In Django, CSS, JavaScript, images, and other external files are referred to as static files. This terminology is used because these files are static, meaning they do not change in response to user inputs or interactions. They remain the same and are served directly to the user's browser without any server-side processing.`

## Key Points:

1. ### Unchanging Content:

- Static files contain fixed content that doesn't change unless manually updated by the developer.

- Examples include stylesheets (CSS), scripts (JavaScript), images, fonts, and other assets that enhance the presentation and functionality of a web application.

2. ### Client-Side Execution:

- These files are sent to the client's browser where they are executed or rendered.

- CSS defines the look and feel of the application, JavaScript provides interactive functionalities, and images and fonts contribute to the visual elements.

3. ### Efficiency:

- Serving static files is efficient because they can be cached by the browser, reducing load times and server requests on subsequent visits.

- Since they are not generated dynamically, they can be delivered quickly to enhance user experience.

4. Django's Handling:

- Django provides tools and configurations to manage and serve static files efficiently.

- The `STATIC_URL, STATICFILES_DIRS and STATIC_ROOT` settings in settings.py help in defining how and where static files are stored and served.

- During development, the `django.contrib.staticfiles `app makes it easy to serve static files locally. In production, these files are typically served by a web server or CDN (Content Delivery Network).

`In settings.py`

#### URL to use when referring to static files

`STATIC_URL = 'static/'`

#### URL to use when referring to user uploaded contents

`MEDIA_URL = '/uploads/'`

#### Directories where Django will look for static files

`STATICFILES_DIRS = [
  BASE_DIR / 'static',
]
`

#### Directory where user uploaded contents will be stored

`MEDIA_ROOT = BASE_DIR / 'static/uploads'`

#### Directory where collected static files will be stored

`STATIC_ROOT = BASE_DIR / 'staticfiles'`

## NEXT PARAMETER

In Django, the next parameter is typically used for redirection purposes. It's a common pattern in authentication flows, especially when you want to redirect users to a specific page after they log in. The next parameter in the URL contains the path to the destination page the user initially attempted to visit before being prompted to log in.

For example, if a user tries to access a restricted page, like `/dashboard`, but isn't logged in, they might be redirected to the login page with a URL like this: `/login/?next=/dashboard`. After successful authentication, your login view can use the next parameter to redirect the user back to `/dashboard`.

#### Here's a brief breakdown:

1. `User Attempts to Access a Restricted Page:` A user tries to go to a page that requires authentication.

2. `Redirection to Login Page with next Parameter:` They are redirected to the login page with the next parameter in the query string, indicating where they wanted to go.

3. `After Login:` Upon successful login, the view retrieves the next parameter value and redirects the user to that page.

Using the next parameter ensures a smooth user experience by taking them directly to the page they intended to visit, rather than a default page.

# DJANGO FILTERS

## Getting Started

Django-filter provides a simple way to filter down a queryset based on parameters a user provides. Say we have a `Product` model and we want to let our users filter which products they see on a list page.

Note

If you’re using django-filter with Django Rest Framework, it’s recommended that you read the [Integration with DRF](https://django-filter.readthedocs.io/en/stable/guide/rest_framework.html#drf-integration) docs after this guide.

## The model

Let’s start with our model:

```
from django.db import models

class Product(models.Model):
name = models.CharField(max_length=255)
price = models.DecimalField(max_digits=5, decimal_places=2)
description = models.TextField()
release_date = models.DateField()
manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
```

## The filter

We have a number of fields and we want to let our users filter based on the name, the price or the release_date. We create a `FilterSet` for this:

import django_filters

class ProductFilter(django_filters.FilterSet):
name = django_filters.CharFilter(lookup_expr='iexact')

    class Meta:
        model = Product
        fields = ['price', 'release_date']

As you can see this uses a very similar API to Django’s `ModelForm`. Just like with a `ModelForm` we can also override filters, or add new ones using a declarative syntax.

### Declaring filters

The declarative syntax provides you with the most flexibility when creating filters, however it is fairly verbose. We’ll use the below example to outline the [core filter arguments](https://django-filter.readthedocs.io/en/stable/ref/filters.html#core-arguments) on a `FilterSet`:

class ProductFilter(django_filters.FilterSet):
price = django_filters.NumberFilter()
price**gt = django_filters.NumberFilter(field_name='price', lookup_expr='gt')
price**lt = django_filters.NumberFilter(field_name='price', lookup_expr='lt')

    release_year = django_filters.NumberFilter(field_name='release_date', lookup_expr='year')
    release_year__gt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__gt')
    release_year__lt = django_filters.NumberFilter(field_name='release_date', lookup_expr='year__lt')

    manufacturer__name = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Product
        fields = ['price', 'release_date', 'manufacturer']

There are two main arguments for filters:

- `field_name`: The name of the model field to filter on. You can traverse “relationship paths” using Django’s `__` syntax to filter fields on a related model. ex, `manufacturer__name`.
- `lookup_expr`: The [field lookup](https://docs.djangoproject.com/en/stable/ref/models/querysets/#field-lookups) to use when filtering. Django’s `__` syntax can again be used in order to support lookup transforms. ex, `year__gte`.

Together, the field `field_name` and `lookup_expr` represent a complete Django lookup expression. A detailed explanation of lookup expressions is provided in Django’s [lookup reference](https://docs.djangoproject.com/en/stable/ref/models/lookups/#module-django.db.models.lookups). django-filter supports expressions containing both transforms and a final lookup.

### Generating filters with Meta.fields

The FilterSet Meta class provides a `fields` attribute that can be used for easily specifying multiple filters without significant code duplication. The base syntax supports a list of multiple field names:

import django_filters

class ProductFilter(django_filters.FilterSet):
class Meta:
model = Product
fields = ['price', 'release_date']

The above generates ‘exact’ lookups for both the ‘price’ and ‘release_date’ fields.

Additionally, a dictionary can be used to specify multiple lookup expressions for each field:

import django_filters

class ProductFilter(django_filters.FilterSet):
class Meta:
model = Product
fields = {
'price': ['lt', 'gt'],
'release_date': ['exact', 'year__gt'],
}

The above would generate ‘price**lt’, ‘price**gt’, ‘release_date’, and ‘release_date**year**gt’ filters.

Note

The filter lookup type ‘exact’ is an implicit default and therefore never added to a filter name. In the above example, the release date’s exact filter is ‘release_date’, not ‘release_date\_\_exact’. This can be overridden by the FILTERS_DEFAULT_LOOKUP_EXPR setting.

Items in the `fields` sequence in the `Meta` class may include “relationship paths” using Django’s `__` syntax to filter on fields on a related model:

class ProductFilter(django_filters.FilterSet):
class Meta:
model = Product
fields = ['manufacturer__country']

#### Overriding default filters

Like `django.contrib.admin.ModelAdmin`, it is possible to override default filters for all the models fields of the same kind using `filter_overrides` on the `Meta` class:

class ProductFilter(django_filters.FilterSet):

    class Meta:
        model = Product
        fields = {
            'name': ['exact'],
            'release_date': ['isnull'],
        }
        filter_overrides = {
            models.CharField: {
                'filter_class': django_filters.CharFilter,
                'extra': lambda f: {
                    'lookup_expr': 'icontains',
                },
            },
            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': forms.CheckboxInput,
                },
            },
        }

### Request-based filtering

The `FilterSet` may be initialized with an optional `request` argument. If a request object is passed, then you may access the request during filtering. This allows you to filter by properties on the request, such as the currently logged-in user or the `Accepts-Languages` header.

Note

It is not guaranteed that a request will be provided to the FilterSet instance. Any code depending on a request should handle the None case.

#### Filtering the primary `.qs`

To filter the primary queryset by the `request` object, simply override the `FilterSet.qs` property. For example, you could filter blog articles to only those that are published and those that are owned by the logged-in user (presumably the author’s draft articles).

class ArticleFilter(django_filters.FilterSet):

    class Meta:
        model = Article
        fields = [...]

    @property
    def qs(self):
        parent = super().qs
        author = getattr(self.request, 'user', None)

        return parent.filter(is_published=True)
            | parent.filter(author=author)

#### Filtering the related queryset for `ModelChoiceFilter`

The `queryset` argument for `ModelChoiceFilter` and `ModelMultipleChoiceFilter` supports callable behavior. If a callable is passed, it will be invoked with the `request` as its only argument. This allows you to perform the same kinds of request-based filtering without resorting to overriding `FilterSet.__init__`.

def departments(request):
if request is None:
return Department.objects.none()

    company = request.user.company
    return company.department_set.all()

class EmployeeFilter(filters.FilterSet):
department = filters.ModelChoiceFilter(queryset=departments)
...

### Customize filtering with `Filter.method`

You can control the behavior of a filter by specifying a `method` to perform filtering. View more information in the [method reference](https://django-filter.readthedocs.io/en/stable/ref/filters.html#filter-method). Note that you may access the filterset’s properties, such as the `request`.

```class F(django_filters.FilterSet):
username = CharFilter(method='my_custom_filter')

    class Meta:
      model = User
      fields = ['username']

      def my_custom_filter(self, queryset, name, value):
          return queryset.filter(**{
              name: value,
          })
```

## The view

Now we need to write a view:

def product_list(request):
f = ProductFilter(request.GET, queryset=Product.objects.all())
return render(request, 'my_app/template.html', {'filter': f})

If a queryset argument isn’t provided then all the items in the default manager of the model will be used.

If you want to access the filtered objects in your views, for example if you want to paginate them, you can do that. They are in f.qs

## The URL conf

We need a URL pattern to call the view:

path('list/', views.product_list, name="product-list")

## The template

```And lastly we need a template:

{% extends "base.html" %}

{% block content %}

<form method="get">
{{ filter.form.as_p }}
<input type="submit" />
</form>
{% for obj in filter.qs %}
{{ obj.name }} - ${{ obj.price }}<br />
{% endfor %}
{% endblock %}
```

And that’s all there is to it! The `form` attribute contains a normal Django form, and when we iterate over the `FilterSet.qs` we get the objects in the resulting queryset.

## Generic view & configuration

In addition to the above usage there is also a class-based generic view included in django-filter, which lives at `django_filters.views.FilterView`. You must provide either a `model` or `filterset_class` argument, similar to `ListView` in Django itself:

# urls.py

from django.urls import path
from django_filters.views import FilterView
from myapp.models import Product

urlpatterns = [
path("list/", FilterView.as_view(model=Product), name="product-list"),
]

If you provide a `model` optionally you can set `filterset_fields` to specify a list or a tuple of the fields that you want to include for the automatic construction of the filterset class.

You must provide a template at `<app>/<model>_filter.html` which gets the context parameter `filter`. Additionally, the context will contain `object_list` which holds the filtered queryset.

A legacy functional generic view is still included in django-filter, although its use is deprecated. It can be found at `django_filters.views.object_filter`. You must provide the same arguments to it as the class based view:

# urls.py

from django.urls import path
from django_filters.views import object_filter
from myapp.models import Product

urlpatterns = [
path("list/", object_filter, {'model': Product}, name="product-list"),
]

The needed template and its context variables will also be the same as the class-based view above.

#### SAMPLE FORM AND FILTERS

```import django_filters
from django_filters import rest_framework as filters
from .models import Profile, Skill

class SkillFilter(filters.FilterSet):
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Skill
        fields = ['name']

class ProfileFilter(filters.FilterSet):
    short_intro = django_filters.CharFilter(lookup_expr='icontains')
    bio = django_filters.CharFilter(lookup_expr='icontains')
    first_name = django_filters.CharFilter(lookup_expr='icontains')
    last_name = django_filters.CharFilter(lookup_expr='icontains')
    skills = django_filters.ModelMultipleChoiceFilter(
        field_name='skill__name',
        to_field_name='name',
        queryset=Skill.objects.all(),
        conjoined=True
    )

    class Meta:
        model = Profile
        fields = ['username', 'location', 'bio', 'short_intro', 'skills']
```

### Steps to Add Skill Filter:

1. **Update the Form in the Template**: Add a dropdown or multiple select input for skills.
2. **Update the View to Handle Skill Filtering**: Modify the view to filter profiles based on the selected skills.

### Updated Form Template:

```html
<form id="searchForm" class="form" action="{% url 'profiles' %}" method="get">
  <div class="form__field">
    <label for="formInput#search">Search Developers </label>
    <input
      class="input input--text"
      id="formInput#search"
      type="text"
      name="search_query"
      value="{{ search_query }}"
      placeholder="Search by developer name"
    />
  </div>

  <div class="form__field">
    <label for="formInput#skills">Filter by Skills</label>
    <select
      class="input input--select"
      id="formInput#skills"
      name="skills"
      multiple
    >
      {% for skill in skills %}
      <option
        value="{{ skill.id }}"
        {%
        if
        skill.id
        in
        selected_skills
        %}selected{%
        endif
        %}
      >
        {{ skill.name }}
      </option>
      {% endfor %}
    </select>
  </div>

  <input class="btn btn--sub btn--lg" type="submit" value="Search" />
</form>
```

### Update the View to Handle Skills:

**views.py**:

```python
from django.shortcuts import render
from .models import Profile, Skill
from .filters import ProfileFilter

def profile_list(request):
    search_query = request.GET.get('search_query', '')
    selected_skills = request.GET.getlist('skills')

    profiles = Profile.objects.all()
    if search_query:
        profiles = profiles.filter(username__icontains=search_query)

    if selected_skills:
        profiles = profiles.filter(skill__id__in=selected_skills).distinct()

    profile_filter = ProfileFilter(request.GET, queryset=profiles)

    context = {
        'profiles': profiles,
        'search_query': search_query,
        'skills': Skill.objects.all(),
        'selected_skills': selected_skills,
        'filter': profile_filter,
    }
    return render(request, 'profile_list.html', context)
```

### Explanation:

1. **Template**:

   - Added a `<select>` element with the `multiple` attribute to allow selection of multiple skills.
   - Populated the select options with skills from the database.
   - Pre-selected skills based on the previously selected options.

2. **View**:
   - Retrieved the `search_query` and `selected_skills` from the GET parameters.
   - Filtered profiles based on the search query and selected skills.
   - Passed the necessary context to the template, including the list of all skills and the selected skills.

This setup should allow you to filter profiles by developer name and skills. Let me know if you need any further assistance or have additional questions! 🚀😊

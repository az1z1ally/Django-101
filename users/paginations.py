from django.http import HttpRequest
from django.core.paginator import Paginator

def paginateProfiles(request: HttpRequest, profiles, pagesize):
  try:
    page_number = int(request.GET.get('page', 1))
  except:
    page_number = 1

  paginator = Paginator(profiles, pagesize)
  page_obj = paginator.get_page(page_number)

  # custom_range = paginator.page_range
  left_index = (page_number - 4) if (page_number - 4) > 1 else 1
  right_index = (page_number + 5) if (page_number + 5) <= paginator.num_pages else paginator.num_pages
  custom_range = range(left_index, right_index + 1)

  return paginator, page_obj, custom_range
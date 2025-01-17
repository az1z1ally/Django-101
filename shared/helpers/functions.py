from django.urls import reverse
from django.utils.http import urlencode
from django.http import HttpRequest

def get_redirect_url(request: HttpRequest, url_name: str):
  """
    Generate a URL with the previous page path as a parameter.
    
    Args:
      url_name (str): The name of the URL pattern to generate the URL for.
      request (HttpRequest): The HTTP request object, used to get the previous page path from the HTTP_REFERER header.
      
    Returns:
      str: The generated URL with the previous page path as a query parameter.
  """
  
  previous_path = request.META.get('HTTP_REFERER', '/')  # Get the previous page from HTTP_REFERER header
  query_params = {'next': previous_path}  # Parameters to include in the URL

  dynamic_url = reverse(url_name)

  # Manually construct the query string
  # query_string = '&'.join([f'{key}={value}' for key, value in query_params.items()])
  query_string = urlencode(query_params)  # Encode a dict or sequence of two-element tuples into a URL query string.
  url_with_parameters = f'{dynamic_url}?{query_string}'  # Generate the URL

  return url_with_parameters



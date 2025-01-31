from sys import stdout
from django.urls import reverse
from django.utils.http import urlencode
from django.http import HttpRequest

import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from django.core.mail import EmailMultiAlternatives
from django.conf import settings

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

# Generate Password
def generate_password(len):
    '''
    This function take an integer(password length) and return random generated password from sample string
    '''

    upper_cases = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    lower_cases = upper_cases.lower()
    digits = '0123456789'
    symbols = '!@#*_'

    all = ''
    upper, lower, nums, syms = True, True, True, True

    if upper:
        all += upper_cases

    if lower:
        all += lower_cases

    if nums:
        all += digits

    if syms:
        all += symbols

    password = ''.join(random.sample(all, len)) # random.sample return a list -- join to get whole sequence in a string
    return password


def send_email(html=None, text='email_body', subject='Hello', from_email=settings.EMAIL_HOST_USER, to_emails=[]):
  assert isinstance(to_emails, list)  # Check to ensure "to_emails" is a list

  # Creating an email with both plain text and HTML versions.
  msg = EmailMultiAlternatives(subject, text, from_email, to_emails)
  
  if html:
    # If HTML content is provided, it's attached as an alternative part of the email(an alternative content representation).
    msg.attach_alternative(html, "text/html")

  # Send the email using Django's EmailBackend
  msg.send(fail_silently=False)

  '''
    When using Django's EmailMultiAlternatives, you don't need to convert the message to a string with msg_str=msg.as_string(). The Django email backend handles all the necessary steps for creating and sending the email.
    The EmailMultiAlternatives class in Django abstracts away a lot of the manual steps you would need to take if you were using smtplib directly. It builds the MIME message, handles attachments, and sends the email using
    the configured email backend in your settings.py.
  '''


# Send email notificaton using python's smptlib directly
def send_email_py(html=None, text='email_body', subject='Hello', from_email=settings.EMAIL_HOST_USER, to_emails=[]):
    assert isinstance(to_emails, list) # An “assert” check here which will raise an error if the “to_emails” argument is not a list
    
    msg=MIMEMultipart('alternative')
    msg['From']=from_email
    msg['To']=", ".join(to_emails)
    msg['Subject']=subject

    txt_part=MIMEText(text, 'plain')
    msg.attach(txt_part)

    if html:
      html_part = MIMEText(html, 'html')
      msg.attach(html_part)

    msg_str=msg.as_string()
    
    try:
      server=smtplib.SMTP(host=settings.EMAIL_HOST, port=settings.EMAIL_PORT)
    except:
      stdout.write(f'Could not establish connection to mail server')
      return

    server.ehlo()

    # Comment these lines if your server does not require authentication and TLS to avoid SMTPNotSupportedError --The command or option attempted is not supported by the server.
    server.starttls()
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)

    # send email
    server.sendmail(from_email, to_emails, msg_str)
    server.quit()

# Example usage
# send_email(html='<h1>Hello</h1>', text='Hello', subject='Greetings', to_emails=['example@example.com'])


# Send SMS for temporary password
def send_sms(msisdn, message):
  pass
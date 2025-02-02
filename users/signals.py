from sys import stdout
from django.db import transaction
from django.db.models.signals import post_save, post_delete, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from shared.helpers.functions import send_email
from .models import Profile

# from django.core.mail import send_mail
from django.conf import settings

User = get_user_model() # Return the user model that is active in this project.

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
  if created:
    user = instance

    # The transaction.atomic() block ensures that all operations within it are atomic—meaning they all succeed or none of them do.
    with transaction.atomic():
      profile = Profile.objects.create(
        user=user,
        username=user.username,
        email=user.email,
        first_name=user.first_name,
        last_name=user.last_name
      )

      subject = 'Welcome to DevSearch'
      message = 'We are glad you are here!'
      html_msg = f'<h1>{message}</h1>'
      to_email = profile.email
      from_email = settings.EMAIL_HOST_USER

      try:
        # send_mail(
        #   subject,
        #   message,
        #   from_email,
        #   [to_email],
        #   fail_silently=False,
        # )

        send_email(html=html_msg, text=message, subject=subject,  from_email=from_email, to_emails=[to_email])
      except:
        stdout.write(f'Email failed to send...')


@receiver(post_save, sender=Profile)
def update_user(sender, instance, created, **kwargs):
  profile = instance
  user = profile.user

  if not created:
    user.first_name = profile.first_name
    user.last_name = profile.last_name
    user.username = profile.username
    user.email = profile.email
    user.save()


# Store the original password before any changes are made.
@receiver(pre_save, sender=User)
def save_original_password(sender, instance, **kwargs):
  try:
    instance._original_password = User.objects.get(pk=instance.pk).password
  except User.DoesNotExist:
    instance._original_password = None


@receiver(post_save, sender=User)
def change_user_password(sender, instance, created, **kwargs):
  if not created:
    original_password = getattr(instance, '_original_password', None)

    # Detect changes to the password field and send notification email if the password has changed
    if original_password and original_password != instance.password:
      subject = 'Devsearch Account Password Change '
      message = 'Your Devsearch account\'s password has been changed, if this was not you kindly change your password immediately.'
      html_msg = f'<h1>{message}</h1>'
      to_email = instance.email
      from_email = settings.EMAIL_HOST_USER

      try:
        send_email(
          html=html_msg,
          text=message,
          subject=subject,
          from_email=from_email,
          to_emails=[to_email]
        )
      except Exception as e:
        stdout.write(f'Email failed to send: {str(e)}')


@receiver(post_delete, sender=Profile)
def delete_user(sender, instance, **kwargs):
  try:
    user = instance.user
    user.delete()
  except Exception as e:
    stdout.write(f'User could not be deleted: {str(e)}')
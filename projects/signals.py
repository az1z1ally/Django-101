from django.db.models.signals import post_delete, post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Review

@receiver([post_save, post_delete], sender=Review)
def get_vote_count(sender, instance, created=None, **kwargs):
  project = instance.project
  project.get_vote_count # Update project vote count


@receiver(pre_save, sender=Review)
def ensure_owner_can_edit(sender, instance, **kwargs):
  if instance.pk:  # Ensure we're updating an existing review
    try:
      original_review = sender.objects.get(pk=instance.pk)
      if instance.owner != original_review.owner:
        raise ValueError('You are not authorized to edit this review. ⚠️⚡')
    except sender.DoesNotExist:
      # Handle the case where the review does not exist
      pass

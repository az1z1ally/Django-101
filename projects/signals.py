from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import Review

@receiver([post_save, post_delete], sender=Review)
def get_vote_count(sender, instance, created=None, **kwargs):
  project = instance.project
  project.get_vote_count # Update project vote count
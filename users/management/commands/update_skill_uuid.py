# users/management/commands/update_skill_uuid.py
from django.core.management.base import BaseCommand
from django.db import transaction
from users.models import Skill
import uuid

class Command(BaseCommand):
    help = 'Update all Skill IDs to random UUIDs'

    @transaction.atomic
    def handle(self, *args, **kwargs):
      skills = Skill.objects.all()
      for skill in skills:
        try:
          # Check if the current ID is a valid UUID
          existing_uuid = uuid.UUID(str(skill.id))
          self.stdout.write(self.style.ERROR(f'Current ID {existing_uuid}'))
        except ValueError:
          # If not, generate a new UUID
          new_uuid = uuid.uuid4()
          skill.id = new_uuid
          try:
            skill.save()
            self.stdout.write(self.style.SUCCESS(f'Successfully updated Skill ID to {new_uuid}'))
          except ValueError as e:
            self.stdout.write(self.style.ERROR(f'Error updating skill {skill.name}: {e}'))
            transaction.set_rollback(True)
            break

      self.stdout.write(self.style.SUCCESS('Update complete'))

# users/management/commands/fix_skill_uuid.py
from django.core.management.base import BaseCommand
from django.db import connection
import uuid

class Command(BaseCommand):
  help = 'Fix malformed UUIDs in Skill table'

  def handle(self, *args, **kwargs):
    with connection.cursor() as cursor:
      cursor.execute('SELECT id, name FROM users_skill')
      rows = cursor.fetchall()
      for row in rows:
        skill_id, skill_name = row
        try:
          # Check if the current ID is a valid UUID
          existing_uuid = uuid.UUID(skill_id)
          self.stdout.write(self.style.SUCCESS(f'Valid UUID: {skill_id}'))
        except ValueError:
          # If not, generate a new UUID
          new_uuid = uuid.uuid4()
          cursor.execute('UPDATE users_skill SET id = %s WHERE id = %s', [str(new_uuid), skill_id])
          self.stdout.write(self.style.SUCCESS(f'Successfully updated Skill ID to {new_uuid}'))

    self.stdout.write(self.style.SUCCESS('Fixing complete'))

from django.db import models
import uuid

class BaseModel(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False) # we remove unique=True, since this is UUID(already unique)
  created_on = models.DateTimeField(auto_now_add=True)
  updated_on = models.DateTimeField(auto_now=True)

  class Meta:
      abstract = True
      ordering = ['-updated_on', '-created_on'] # -ve for descending order
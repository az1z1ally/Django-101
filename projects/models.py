from django.db import models
from django.forms import ValidationError
from shared.models import BaseModel

# Create your models here.
class Project(BaseModel):
  title = models.CharField(max_length=200)
  description = models.TextField(null=True, blank=True)
  demo_link = models.CharField(max_length=2000, null=True, blank=True)
  source_link = models.CharField(max_length=2000, null=True, blank=True)
  tags = models.ManyToManyField('Tag', blank=True)
  votes_total = models.IntegerField(default=0, null=True, blank=True)
  votes_ratio = models.IntegerField(default=0, null=True, blank=True)

  def __str__(self):
    return self.title
  

class Review(BaseModel):
  VOTE_TYPE = (
    ('up', 'Up Vote'),
    ('down', 'Down Vote')
  )

  # owner = 
  project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='reviews')
  body = models.TextField(null=True, blank=True)
  value = models.CharField(max_length=20, choices=VOTE_TYPE)

  def __str__(self):
    return self.value
  

class Tag(BaseModel):
  name = models.CharField(max_length=32, unique=True)

  # Enforce case-insensitive uniqueness
  def save(self, *args, **kwargs):
    # self.name = self.name.lower()
    if Tag.objects.filter(name__iexact=self.name).exists():
      raise ValidationError(f'Tag "{self.name}" already exists.')
    super(Tag, self).save(*args, **kwargs)

  def __str__(self):
    return self.name
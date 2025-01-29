from django.db import models
from django.core.exceptions import ValidationError
from shared.models import BaseModel
from users.models import Profile

# Create your models here.
class Project(BaseModel):
  owner = models.ForeignKey(Profile, on_delete=models.SET_NULL, related_name='projects', null=True, blank=True)
  title = models.CharField(max_length=200)
  description = models.TextField(null=True, blank=True)
  featured_image = models.ImageField(null=True, blank=True, default='default.jpg')
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
  def clean(self):
    # self.name = self.name.lower()
    if Tag.objects.filter(name__iexact=self.name).exists():
      raise ValidationError(f'Tag "{self.name}" already exists.')

  def save(self, *args, **kwargs):
    self.full_clean() # This will call the clean() method
    super(Tag, self).save(*args, **kwargs)

  def __str__(self):
    return self.name
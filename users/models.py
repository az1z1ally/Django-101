from django.contrib.auth import get_user_model
from django.db import models
from django.core.exceptions import ValidationError

from shared.models import BaseModel

# Create your models here.
User = get_user_model() # Return the user model that is active in this project.

class Profile(BaseModel):
  user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
  username = models.CharField(max_length=200, unique=True, blank=True, null=True)
  email = models.EmailField(max_length=200, unique=True, null=True, blank=True)
  first_name = models.CharField(max_length=200, blank=True, null=True)
  last_name = models.CharField(max_length=200, blank=True, null=True)
  location = models.CharField(max_length=200, blank=True, null=True, default='Earth')
  short_intro = models.CharField(max_length=200, blank=True, null=True, default='This is a default intro. The user has not added an intro yet.')
  bio = models.TextField(blank=True, null=True)
  profile_image = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
  social_github = models.CharField(max_length=200, blank=True, null=True)
  social_x = models.CharField(max_length=200, blank=True, null=True)
  social_linkedin = models.CharField(max_length=200, blank=True, null=True)
  social_youtube = models.CharField(max_length=200, blank=True, null=True)
  personal_website = models.CharField(max_length=200, blank=True, null=True)

  def __str__(self):
    return str(self.username) # wrapped username into a str() to ensure we always get back a string since it can be null.

  @property
  def imageURL(self):
    try:
      url = self.profile_image.url
    except:
      url = ''
    return url
  
  # Enforce case-sensitive uniqueness
  def save(self, *args, **kwargs):
    self.username = self.username.lower()
    self.email = self.email.lower()
    
    super(Profile, self).save(*args, **kwargs)
  

class Skill(BaseModel):
  owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=32, blank=True, null=True)
  description = models.TextField(null=True, blank=True)

  class Meta:
    unique_together = (('owner', 'name'),)  # Ensure unique skill names per user if required

  # Prevent adding more than 10 skills
  def clean(self):
    if self.owner:
      skills_count = self.owner.skill_set.exclude(pk=self.pk).count() # Without excluding self.pk, it will be counted in count & prevent even editing
      if skills_count >= 10:
        raise ValidationError('You cannot add more than 10 skills.')
  
  def save(self, *args, **kwargs):
    self.full_clean() # This will call the clean() method
    super(Skill, self).save(*args, **kwargs)

  def __str__(self):
    return str(self.name)
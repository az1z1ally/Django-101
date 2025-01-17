from django.contrib.auth import get_user_model
from django.db import models
from django.forms import ValidationError

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
  
  # Enforce case-insensitive uniqueness
  def save(self, *args, **kwargs):
    self.username = self.username.lower()
    self.email = self.email.lower()

    if Profile.objects.filter(username__iexact=self.username).exists():
      raise ValidationError(f'"{self.username}" already exists.')
    
    if Profile.objects.filter(email__iexact=self.email).exists():
      raise ValidationError(f'"{self.email}" already exists.')
    
    super(Profile, self).save(*args, **kwargs)
  

class Skill(models.Model):
  owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
  name = models.CharField(max_length=200, blank=True, null=True)
  description = models.TextField(null=True, blank=True)

  def __str__(self):
    return str(self.name)
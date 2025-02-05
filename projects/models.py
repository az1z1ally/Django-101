from django.db import models
from django.core.exceptions import ValidationError
from shared.models import BaseModel
from shared.types.enums import VoteType
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

  class Meta:
    ordering = ['-votes_ratio', '-votes_total', '-updated_on']

  def __str__(self):
    return self.title
  
  @property
  def get_reviewers_ids(self):
    reviewers_ids = self.project_reviews.values_list('owner__id', flat=True) # Get the owner IDs for reviews of this project
    return reviewers_ids
  
  @property
  def get_vote_count(self):
    reviews = self.project_reviews.all()
    total_votes = reviews.count()
    up_votes = reviews.filter(value=VoteType.UP.value).count()
    positive_ratio = (up_votes / total_votes) * 100

    self.votes_total = total_votes
    self.votes_ratio = positive_ratio
    
    self.save()
  

class Review(BaseModel):
  owner = models.ForeignKey(Profile, on_delete=models.CASCADE, blank=True, null=True, related_name='owner_reviews')
  project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='project_reviews')
  body = models.TextField(null=True, blank=True)
  value = models.CharField(max_length=20, choices=[(vote.value, vote.name) for vote in VoteType])

  class Meta:
    unique_together = (('owner', 'project'),)  # Ensure user can submit only one review(no two instances of the reviews belongs to the same owner on the same project)

  def clean(self):
    # Ensure user can not review their own project
    if self.owner and self.owner == self.project.owner:
      raise ValidationError(f'You can not review your own project!')

  def save(self, *args, **kwargs):
    self.full_clean() # This will call the clean() method
    super(Review, self).save(*args, **kwargs)

  def __str__(self):
    return f'{self.value}__{self.project.title[:32]}'
  

class Tag(BaseModel):
  name = models.CharField(max_length=32, unique=True)

  # Enforce case-insensitive uniqueness
  def clean(self):
    if Tag.objects.filter(name__iexact=self.name).exists():
      raise ValidationError(f'Tag "{self.name}" already exists.')

  def save(self, *args, **kwargs):
    self.full_clean() # This will call the clean() method
    super(Tag, self).save(*args, **kwargs)

  def __str__(self):
    return self.name
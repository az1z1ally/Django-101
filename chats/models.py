from django.db import models

from shared.models import BaseModel
from users.models import Profile

# Create your models here.
class Message(BaseModel):
  sender = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_msgs')
  recipient = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True, related_name='received_msgs')
  sender_name = models.CharField(max_length=80, null=True, blank=True)
  email= models.EmailField(max_length=200, null=True, blank=True)
  subject = models.CharField(max_length=200, null=True, blank=True)
  body = models.TextField()
  is_read = models.BooleanField(default=False, null=True)

  class Meta:
    ordering = ['is_read', '-created_on']

  def __str__(self):
    return f'{str(self.sender_name)} ** {self.created_on}'
  
  def get_unread_messages_count(self, recipient_profile):
    # Filter unread messages for the specified recipient
    unread_messages = Message.objects.filter(recipient=recipient_profile, is_read=False)
    
    # Return the count of unread messages
    return unread_messages.count()

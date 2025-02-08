from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import MessageForm
from users.models import Profile

# Create your views here.

@login_required(login_url='login')
def inbox(request):
  profile = request.user.profile
  received_msgs = profile.received_msgs.all()
  unread_msgs_count = received_msgs.filter(is_read=False).count()

  context = {'received_msgs': received_msgs, 'unread_msgs_count': unread_msgs_count}
  return render(request, 'chats/inbox.html', context)


@login_required(login_url='login')
def viewMessage(request, message_id):
  profile = request.user.profile
  try:
    message = profile.received_msgs.get(id=message_id)
  except Exception as e:
    return render(request, '404.html', status=404)
  
  if not message.is_read:
    message.is_read = True
    message.save()

  context = {'message': message}
  return render(request, 'chats/message.html', context)


# Send message view
def sendMessage(request, recipient_id):
  try:
    recipient = Profile.objects.get(id=recipient_id)
  except Exception as e:
    return render(request, '404.html', status=404)
  
  try:
    sender = request.user.profile
  except:
    sender = None
  
  form = MessageForm()
  
  if request.method == 'POST':
    form = MessageForm(request.POST)
    if form.is_valid():
      message = form.save(commit=False)
      message.sender = sender
      message.recipient = recipient

      if sender:
        message.sender_name = f'{sender.first_name} {sender.last_name}'
        message.email = sender.email
      message.save()

      messages.success(request, 'Message sent successfully. 👍✅')
      return redirect('profile', pk=recipient.id)
    
    else:
      messages.error(request, 'Failed to send a message! ⚠️⚡')
  
  context = {'recipient': recipient, 'form': form}
  return render(request, 'chats/message_form.html', context)
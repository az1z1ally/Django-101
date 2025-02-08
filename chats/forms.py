from .models import Message
from django.forms import ModelForm


class MessageForm(ModelForm):
  class Meta:
    model = Message
    fields = ['sender_name', 'email', 'subject', 'body']

  def __init__(self, *args, **kwargs):
    super(MessageForm, self).__init__(*args, **kwargs)

    for name, field in self.fields.items():
      field.widget.attrs.update({'class': 'input'})

      if name == 'body':
        field.widget.attrs.update({'class': 'input input--textarea'})
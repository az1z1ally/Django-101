# Generated by Django 5.1.4 on 2025-02-08 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chats', '0002_rename_name_message_sender_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='message',
            name='email',
            field=models.EmailField(max_length=200),
        ),
    ]

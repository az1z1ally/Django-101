# Generated by Django 5.1.4 on 2025-01-08 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_rename_website_profile_personal_website'),
    ]

    operations = [
        migrations.RenameField(
            model_name='skill',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='skill',
            name='last_name',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]

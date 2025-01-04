# Generated by Django 5.1.4 on 2025-01-04 11:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_project_featured_image_alter_tag_name'),
        ('users', '0002_profile_website'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='projects', to='users.profile'),
        ),
    ]

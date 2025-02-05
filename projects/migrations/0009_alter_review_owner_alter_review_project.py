# Generated by Django 5.1.4 on 2025-02-04 11:44

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0008_alter_review_options_review_owner_and_more'),
        ('users', '0011_alter_skill_options_alter_skill_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='owner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='owner_reviews', to='users.profile'),
        ),
        migrations.AlterField(
            model_name='review',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_reviews', to='projects.project'),
        ),
    ]

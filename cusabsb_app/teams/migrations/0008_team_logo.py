# Generated by Django 4.1.6 on 2023-02-09 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_remove_team_logo'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to='team_logos'),
        ),
    ]

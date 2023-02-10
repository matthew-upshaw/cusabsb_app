# Generated by Django 4.1.6 on 2023-02-10 13:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0009_team_logo_svg'),
    ]

    operations = [
        migrations.AddField(
            model_name='team',
            name='bsb_page',
            field=models.CharField(default='placeholder', max_length=255),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='year_joined',
            field=models.CharField(default='2020', max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='team',
            name='year_left',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
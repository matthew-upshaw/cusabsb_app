# Generated by Django 4.1.6 on 2023-02-07 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_pitcher_whip'),
    ]

    operations = [
        migrations.AddField(
            model_name='batter',
            name='is_latest',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='fielder',
            name='is_latest',
            field=models.BooleanField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pitcher',
            name='is_latest',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
    ]

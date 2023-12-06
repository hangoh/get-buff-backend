# Generated by Django 4.2.7 on 2023-12-03 12:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('badges', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='streak_count_required',
            field=models.PositiveIntegerField(default=1, help_text='only used for streak traking type to indicate how much count it need to get 1 streak progression'),
        ),
    ]
# Generated by Django 4.2.7 on 2023-11-25 09:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('training', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customtrainingset',
            old_name='type',
            new_name='training_type',
        ),
        migrations.AddField(
            model_name='customtrainingset',
            name='min_count',
            field=models.PositiveIntegerField(default=5),
        ),
        migrations.AddField(
            model_name='exercise',
            name='min_count',
            field=models.PositiveIntegerField(default=0, help_text='minimum number of reps or seconds need to init for this exercise'),
        ),
    ]

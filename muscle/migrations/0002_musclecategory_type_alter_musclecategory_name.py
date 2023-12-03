# Generated by Django 4.2.7 on 2023-12-03 12:06

from django.db import migrations, models
import enumfields.fields
import muscle.enums


class Migration(migrations.Migration):

    dependencies = [
        ('muscle', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='musclecategory',
            name='type',
            field=enumfields.fields.EnumField(default='NON', enum=muscle.enums.MuscleGroup, max_length=3),
        ),
        migrations.AlterField(
            model_name='musclecategory',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]

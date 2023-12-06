# Generated by Django 4.2.7 on 2023-12-03 11:34

import badges.enums
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import muscle.enums
import training.enums


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Badge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=512)),
                ('image', models.URLField()),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Track',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('special_target', enumfields.fields.EnumField(default='NON', enum=badges.enums.SpecialTargetType, help_text='[streak - to track about a continuous action]  [none - default for non streak target]  ', max_length=3)),
                ('type_target', enumfields.fields.EnumField(enum=training.enums.TrainingOrExerciseType, max_length=3)),
                ('level_target', enumfields.fields.EnumField(enum=training.enums.TrainingLevel, max_length=3)),
                ('muscle_target', enumfields.fields.EnumField(enum=muscle.enums.MuscleGroup, max_length=3)),
                ('count_type', enumfields.fields.EnumField(enum=badges.enums.TargetCountType, max_length=3)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='UserAchivementBadge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('desp', models.TextField(help_text='Description about the badge and how to earn progress for it')),
                ('progress_count', models.PositiveIntegerField(default=0)),
                ('obtain_time', models.DateTimeField(blank=True, null=True)),
                ('is_obtained', models.BooleanField(default=False)),
                ('required_value', models.PositiveIntegerField(help_text='Description about the progression count needed to obtain the achivement badge')),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='badges.badge')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='badges.track')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='user.userprofile')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SkeletonAchivementBadge',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('desp', models.TextField(help_text='Description about the badge and how to earn progress for it')),
                ('required_value', models.PositiveIntegerField(help_text='Description about the progression count needed to obtain the achivement badge')),
                ('badge', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='badges.badge')),
                ('track', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='badges.track')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
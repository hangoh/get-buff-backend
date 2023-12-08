# Generated by Django 4.2.7 on 2023-12-07 16:15

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import enumfields.fields
import user.enums
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('training', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female')], default='male', max_length=10)),
                ('dob', models.DateField(blank=True, null=True)),
                ('weight_in_kg', models.DecimalField(blank=True, decimal_places=2, default=60.0, max_digits=5, null=True)),
                ('height_in_cm', models.PositiveIntegerField(blank=True, default=170, null=True)),
                ('target_weight_in_kg', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('weight_target_status', enumfields.fields.EnumField(default='MAN', enum=user.enums.TargetStatus, max_length=10)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rest_time', models.PositiveIntegerField(default=25, help_text='rest time setting between exercise, calculated in seconds and should not exceed 120 seconds')),
                ('user_profile', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile')),
            ],
        ),
        migrations.CreateModel(
            name='TrainingSetCompletedRecord',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completed_date_time', models.DateTimeField(auto_now_add=True)),
                ('training_set', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='training.customtrainingset')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.userprofile')),
            ],
        ),
        migrations.AddConstraint(
            model_name='userprofile',
            constraint=models.CheckConstraint(check=models.Q(('height_in_cm__gt', 0), ('height_in_cm__lte', 350)), name='height_in_cm_range_check'),
        ),
        migrations.AddConstraint(
            model_name='userprofile',
            constraint=models.CheckConstraint(check=models.Q(('weight_in_kg__gt', 0.0), ('weight_in_kg__lte', 500.0)), name='weight_in_kg_range_check'),
        ),
        migrations.AddConstraint(
            model_name='userprofile',
            constraint=models.CheckConstraint(check=models.Q(('weight_in_kg__gt', 0.0), ('weight_in_kg__lte', 500.0)), name='target_weight_in_kg_range_check'),
        ),
        migrations.AddConstraint(
            model_name='trainingsetting',
            constraint=models.CheckConstraint(check=models.Q(('rest_time__gte', 5), ('rest_time__lte', 120)), name='rest_time_range_check'),
        ),
    ]

# Generated by Django 4.2.7 on 2023-11-28 12:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0006_remove_trainingsetting_rest_time_range_check_and_more'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='userprofile',
            name='height_in_cm_range_check',
        ),
        migrations.RemoveConstraint(
            model_name='userprofile',
            name='weight_in_kg_range_check',
        ),
        migrations.RemoveConstraint(
            model_name='userprofile',
            name='target_weight_in_kg_range_check',
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
    ]

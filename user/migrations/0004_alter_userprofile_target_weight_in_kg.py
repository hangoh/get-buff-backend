# Generated by Django 4.2.7 on 2023-12-10 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_userprofile_height_in_cm'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='target_weight_in_kg',
            field=models.DecimalField(blank=True, decimal_places=2, default=60.0, max_digits=5, null=True),
        ),
    ]

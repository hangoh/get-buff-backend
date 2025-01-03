import uuid

from django.db import models
from django.db.models.constraints import CheckConstraint

from enumfields import EnumField

from account.models import User
from user.enums import TargetStatus


# Create your models here.
GENDER_CHOICES=[
    ("male", 'male'), 
    ("female", "female"), 
]


class BaseModel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        

class UserProfile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, default="male")
    dob = models.DateField(null=True, blank=True)
    weight_in_kg = models.DecimalField(
        null=True,
        blank=True, 
        max_digits=5, 
        decimal_places=2,
        default=60.00
    )
    height_in_cm = models.IntegerField(
        null=True,
        blank=True,
        default=170
    )
    target_weight_in_kg = models.DecimalField(
        default=60.00,
        null=True,
        blank=True,
        max_digits=5,
        decimal_places=2,
    )
    weight_target_status = EnumField(
        TargetStatus, 
        default=TargetStatus.MAINTAIN
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=models.Q(height_in_cm__gt=50,
                               height_in_cm__lte=350),
                name='height_in_cm_range_check'
            ),
            CheckConstraint(
                check=models.Q(weight_in_kg__gt=0.00,
                               weight_in_kg__lte=500.00),
                name='weight_in_kg_range_check'
            ),
            CheckConstraint(
                check=models.Q(weight_in_kg__gt=0.00,
                               weight_in_kg__lte=500.00),
                name='target_weight_in_kg_range_check'
            ),
        ]

    def __str__(self):
        return f"[{self.id}] {self.user.first_name} {self.user.last_name} - {self.gender}"
    

class TrainingSetCompletedRecord(models.Model):
    """
    Act like a record for completed training set, not really being use 
    """
    user_profile = models.ForeignKey(
        UserProfile, null=False, blank=False, on_delete=models.CASCADE
    )
    completed_date_time = models.DateTimeField(auto_now_add=True)
    training_set = models.OneToOneField(
        "training.CustomTrainingSet",
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return (
            f"{self.user_profile.user.first_name} {self.user_profile.user.last_name} - "
            f"{self.training_set.name} - {self.completed_date_time}"
        )
    

class TrainingSetting(models.Model):
    user_profile = models.OneToOneField(
        UserProfile, null=False, blank=False, on_delete=models.CASCADE
    )
    rest_time = models.PositiveIntegerField(
        default=25,
        help_text="rest time setting between exercise, calculated in seconds and should not exceed 120 seconds"
    )

    class Meta:
        constraints = [
            CheckConstraint(
                check=models.Q(rest_time__gte=5,
                               rest_time__lte=120),
                name='rest_time_range_check'
            ),
        ]
    
    def __str__(self):
        return (
            f"{self.user_profile.user.first_name} {self.user_profile.user.last_name} - "
            f"rest time: {self.rest_time}s"
        )

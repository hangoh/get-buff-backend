from datetime import datetime

from urllib.parse import urljoin
from django.urls import reverse

from freezegun import freeze_time

from rest_framework.test import APITestCase
from rest_framework.authtoken.models import Token
from user.models import (
    UserProfile,
    TrainingSetting,
    TrainingSetCompletedRecord
)
from training.models import(
    CustomTrainingSet,
)
from muscle.models import (
    MuscleCategory
)
from training.enums import (
    TrainingLevel,
    TrainingType,
    TrainingStatus
)
from user.enums import TargetStatus
from muscle.enums import MuscleGroup
from account.models import User


class TestUserProfile(APITestCase):
    SIGN_UP_USER_URL = reverse('api:account:user_sign_up')
    USER_PROFILE_URL = reverse('api:user:user_profile-list')
    TRAINING_SETTING_URL = reverse('api:user:training_setting')
    TRAINING_HISTORY = reverse('api:user:training_history')
    CALORIES = reverse('api:user:calories')

    def setUp(self):
        user = User.objects.create_user(
            email = "uncleben@gmail.com",
            password = "JustPassword123",
            first_name =  "Uncle",
            last_name =  "Ben",
        )
        UserProfile.objects.filter(
            user = user
        ).update(
            gender = "male",
            weight_in_kg = 50.10,
            height_in_cm = 173,
            target_weight_in_kg=50.10)
        token = Token.objects.create(user=user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {token.key}')

    def test_view_user_profile_list(self):
        resp = self.client.get(self.USER_PROFILE_URL)
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(
            resp.json()[0],
            {
                "first_name": "Uncle",
                "last_name": "Ben",
                "gender":"male",
                "weight_in_kg":"50.10",
                "height_in_cm":173,
                "target_weight_in_kg":"50.10",
                "weight_target_status":"maintain",
                "uuid":str(UserProfile.objects.all().first().uuid)
            }
        )
    
    def test_view_user_profile_retrieve(self):
        resp = self.client.get(
            urljoin(self.USER_PROFILE_URL,f"{UserProfile.objects.all().first().id}/")
        )
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(
            resp.json(),
            {
                "first_name": "Uncle",
                "last_name": "Ben",
                "gender":"male",
                "weight_in_kg":"50.10",
                "height_in_cm":173,
                "target_weight_in_kg":"50.10",
                "weight_target_status":"maintain",
                "uuid":str(UserProfile.objects.all().first().uuid)
            }
        )

    def test_update_user_profile(self):
        data={
            "gender":"male",
            "weight_in_kg":600,
            "height_in_cm":173,
            "target_weight_in_kg":80,
        }
        resp = self.client.post(self.USER_PROFILE_URL, data, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertDictEqual(
            resp.json()['data'],
            {
                "first_name": "Uncle",
                "last_name": "Ben",
                "gender":"male",
                "weight_in_kg":"60.00",
                "height_in_cm":173,
                "target_weight_in_kg":"80.00",
                "weight_target_status":"gain",
                "uuid":str(UserProfile.objects.all().first().uuid)
            }
        )

    def test_training_setting_get(self):
        resp = self.client.get(self.TRAINING_SETTING_URL)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['data']['rest_time'],25)

    def test_training_setting_update(self):
        data={
            "profile":UserProfile.objects.all().first().uuid,
            "rest_time":15
        }
        resp = self.client.post(self.TRAINING_SETTING_URL, data, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['data']['rest_time'],15)
        self.assertEqual(
            TrainingSetting.objects.all().first().rest_time,
            15
        )

    def test_training_setting_over_max_update(self):
        data={
            "profile":UserProfile.objects.all().first().uuid,
            "rest_time":15000000
        }
        resp = self.client.post(self.TRAINING_SETTING_URL, data, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['data']['rest_time'],25)
        self.assertEqual(
            TrainingSetting.objects.all().first().rest_time,
            25
        )

    def test_training_setting_invalid_format_update(self):
        data={
            "profile":UserProfile.objects.all().first().uuid,
            "rest_time":"150000sdf00"
        }
        resp = self.client.post(self.TRAINING_SETTING_URL, data, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['error'],"Invalid data format or type")

    def test_training_setting_invalid_profile_update(self):
        data={
            "profile":34534563456345,
            "rest_time":"150000sdf00"
        }
        resp = self.client.post(self.TRAINING_SETTING_URL, data, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(resp.json()['error'],"Error on authentication, please logout and login again")

    @freeze_time("2023-11-21 12:00:00")
    def test_training_history_view(self):
        muscle_cat = MuscleCategory.objects.create(name=MuscleGroup.BACKNSHOULDER, image_url="http://test")
        CustomTrainingSet.objects.create(
            user_profile = UserProfile.objects.all().first(),
            name = "test custom preset",
            level =TrainingLevel.ADVANCE,
            muscle_category = muscle_cat,
            status = TrainingStatus.COMPLETED,
            training_type = TrainingType.PRESET
        )
        CustomTrainingSet.objects.create(
            user_profile = UserProfile.objects.all().first(),
            name = "test custom ",
            level =TrainingLevel.ADVANCE,
            status = TrainingStatus.GIVEUP,
            training_type = TrainingType.CUSTOM
        )

        resp = self.client.get(
            urljoin(self.TRAINING_HISTORY, "?date=2023-11-30")
        )
        self.assertEqual(
            resp.status_code, 
            200
        )

    def test_calories_view_error(self):
        resp = self.client.get(self.CALORIES)
        self.assertEqual(resp.status_code, 400)
        self.assertEqual(
            resp.json()['error'],
            "Please provide your weight(kg), height(cm), gender and date of birth to calculate your calories needed"
        )

    @freeze_time("2023-12-01 12:00:00")
    def test_calories_view(self):
        user_profile = UserProfile.objects.all().first()
        user_profile.dob = datetime.strptime("2000-01-01", '%Y-%m-%d')
        user_profile.weight_target_status = TargetStatus.GAIN
        user_profile.save()
        for i in range(5):
            cts = CustomTrainingSet.objects.create(
                user_profile=user_profile,
                name=f'custom-training-{i+1}',
                status = TrainingStatus.COMPLETED, 
                training_type =TrainingType.PRESET
            )
            TrainingSetCompletedRecord.objects.create(
                user_profile= user_profile,
                training_set = cts
            )
        resp = self.client.get(urljoin(self.CALORIES, "?kg_gain_lost=1"))
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json()['calories'], 3382)
        

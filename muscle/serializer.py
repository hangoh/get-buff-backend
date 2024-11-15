from rest_framework import serializers

from training.models import (
    MuscleCategory,
    Muscle
)


class MuscleCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleCategory
        fields = (
            'id',
            'name',
            'type',
            'image_url'
        )

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['type'] = instance.get_type_display()
        return representation


class MuscleSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Muscle
        fields = (
            "id",
            "name",
            "front_image_url",
            "back_image_url", 
        )
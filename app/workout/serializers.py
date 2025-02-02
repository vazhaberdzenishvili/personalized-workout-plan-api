from rest_framework import serializers
from core.models import MuscleGroup


class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']

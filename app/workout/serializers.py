from rest_framework import serializers
from core.models import (
    MuscleGroup,
    Exercise,
    WorkoutPlan
)
from typing import List


class MuscleGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = MuscleGroup
        fields = ['id', 'name', 'description']
        read_only_fields = ['id']


class ExerciseSerializer(serializers.ModelSerializer):
    target_muscles = serializers.PrimaryKeyRelatedField(
        many=True, queryset=MuscleGroup.objects.all(), write_only=True
    )
    target_muscle_names = serializers.SerializerMethodField()

    class Meta:
        model = Exercise
        fields = ['id', 'name', 'description', 'instructions',
                  'target_muscles', 'target_muscle_names']
        read_only_fields = ['id']

    def create(self, validated_data):
        target_muscles_data = validated_data.pop('target_muscles', [])
        exercise = Exercise.objects.create(**validated_data)
        if target_muscles_data:
            exercise.target_muscles.set(target_muscles_data)
        return exercise

    def get_target_muscle_names(self, obj) -> List[str]:
        """Return a list of muscle names."""
        return [muscle.name for muscle in obj.target_muscles.all()]


class WorkoutPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = [
            'id',
            'user',
            'name',
            'frequency',
            'goal',
            'duration_per_session'
        ]
        read_only_fields = ['id', 'user']

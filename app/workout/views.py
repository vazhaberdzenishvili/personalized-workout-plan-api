from rest_framework import viewsets

from core.models import (
    MuscleGroup,
    Exercise
)
from workout import serializers


class MuscleGroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MuscleGroupSerializer
    queryset = MuscleGroup.objects.all()


class ExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ExerciseSerializer
    queryset = Exercise.objects.all()

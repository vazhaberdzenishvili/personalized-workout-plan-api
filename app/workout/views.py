from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly

from core.models import (
    MuscleGroup,
    Exercise
)
from workout import serializers


class MuscleGroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MuscleGroupSerializer
    queryset = MuscleGroup.objects.all()
    permission_classes = [IsAdminOrReadOnly]


class ExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ExerciseSerializer
    queryset = Exercise.objects.all()
    permission_classes = [IsAdminOrReadOnly]

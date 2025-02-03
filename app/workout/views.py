from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated

from core.models import (
    MuscleGroup,
    Exercise,
    WorkoutPlan
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


class WorkoutPlanViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WorkoutPlanSerializer
    queryset = WorkoutPlan.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('name')

    def perform_create(self, serializer):
        """Create a new workout plan."""
        serializer.save(user=self.request.user)

from rest_framework import viewsets
from .permissions import IsAdminOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, OpenApiExample

from core.models import (
    MuscleGroup,
    Exercise,
    WorkoutPlan,
    WorkoutPlanExercise,
    WorkoutSession,
    Progress
)
from workout import serializers


@extend_schema(tags=['Muscle groups'])
class MuscleGroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MuscleGroupSerializer
    queryset = MuscleGroup.objects.all()
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(tags=['Exercises'])
class ExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ExerciseSerializer
    queryset = Exercise.objects.all()
    permission_classes = [IsAdminOrReadOnly]


@extend_schema(
    tags=['Workout Plans'],
    description="Create a new workout plan",
    examples=[
        OpenApiExample(
            "Workout Plan Example",
            value={
                "name": "Full Body Strength",
                "frequency": 3,
                "goal": "Build muscle & strength",
                "duration_per_session": "01:00:00"
            },
            request_only=True,
        )
    ],
    responses={201: serializers.WorkoutPlanSerializer}
)
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


@extend_schema(
    tags=['Workout Plan Exercises'],
    description="Create a new workout plan exercise",
    examples=[
        OpenApiExample(
            "Workout Plan Exercise Example",
            value={
                "repetitions": 12,
                "sets": 4,
                "duration": "00:45:00",
                "distance": 5.2,
                "workout_plan": 1,
                "exercise": 3
            },
            request_only=True,
        )

    ],
    responses={201: serializers.WorkoutPlanExerciseSerializer}
)
class WorkoutPlanExerciseViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WorkoutPlanExerciseSerializer
    queryset = WorkoutPlanExercise.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(workout_plan__user=self.request.user)

    def perform_create(self, serializer):
        workout_plan_id = self.request.data.get('workout_plan')
        workout_plan = get_object_or_404(WorkoutPlan,
                                         id=workout_plan_id,
                                         user=self.request.user)
        serializer.save(workout_plan=workout_plan)


@extend_schema(
    tags=['Workout Sessions'],
    description="Create a new workout session",
    examples=[
        OpenApiExample(
            "Workout Session Example",
            value={
                "workout_plan": 1,
                "date": "2025-01-01",
                "completed": False
            },
            request_only=True,
        )
    ],
    responses={201: serializers.WorkoutSessionSerializer}

)
class WorkoutSessionViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.WorkoutSessionSerializer
    queryset = WorkoutSession.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def perform_create(self, serializer):
        """Create a new workout session"""
        serializer.save(user=self.request.user)


@extend_schema(tags=['Progress Tracking'])
class ProgressViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ProgressSerializer
    queryset = Progress.objects.all()
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user).order_by('-date')

    def perform_create(self, serializer):
        """Create a new Progress record"""
        serializer.save(user=self.request.user)

from django.urls import (
    path,
    include,
)
from rest_framework.routers import DefaultRouter
from workout import views

router = DefaultRouter()
router.register('muscle_groups', views.MuscleGroupViewSet,
                basename='muscle-group')
router.register('exercises', views.ExerciseViewSet,
                basename='exercise')
router.register(
    'workout_plan', views.WorkoutPlanViewSet, basename='workout-plan'
)
router.register(
    'workout_plan_exercise',
    views.WorkoutPlanExerciseViewSet,
    basename='workout-plan-exercise'
)

app_name = 'workout'

urlpatterns = [
    path('', include(router.urls))
]

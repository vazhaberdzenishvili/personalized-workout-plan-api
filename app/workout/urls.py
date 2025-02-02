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

app_name = 'workout'

urlpatterns = [
    path('', include(router.urls))
]

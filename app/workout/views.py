from rest_framework import viewsets

from core.models import (
    MuscleGroup,
)
from workout import serializers


class MuscleGroupViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.MuscleGroupSerializer
    queryset = MuscleGroup.objects.all()

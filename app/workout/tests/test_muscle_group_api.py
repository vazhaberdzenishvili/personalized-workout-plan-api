from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from core.models import MuscleGroup
from workout.serializers import MuscleGroupSerializer


def muscle_group_url():
    """Return the muscle group list URL"""
    return reverse('workout:muscle-group-list')


class MuscleGroupAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='user@example.com', password='password123'
        )
        self.muscle_group = MuscleGroup.objects.create(
            name="Biceps",
            description="Muscles in the upper arm, responsible for arm flexion"
        )

    def test_retrieve_muscle_groups(self):
        """Test retrieving a list of muscle groups"""
        self.client.force_authenticate(user=self.user)
        res = self.client.get(muscle_group_url())
        expected = MuscleGroup.objects.all().order_by('id')
        serializer = MuscleGroupSerializer(expected, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

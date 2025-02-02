from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from core.models import Exercise, MuscleGroup
from workout.serializers import ExerciseSerializer


def exercise_url():
    """Return the exercise list URL"""
    return reverse('workout:exercise-list')


class ExerciseAPITest(APITestCase):
    """Test case for the Exercise API"""

    def setUp(self):
        self.client = APIClient()

        self.user = get_user_model().objects.create_user(
            email='user@example.com', password='password123'
        )
        self.muscle_group = MuscleGroup.objects.create(
            name="Biceps", description="Muscles in the upper arm")
        self.exercise = Exercise.objects.create(
            name="Bicep Curl",
            description="A basic bicep exercise.",
        )
        self.exercise.target_muscles.set([self.muscle_group])

    def test_retrieve_exercises(self):
        """Test that a normal user can retrieve exercises"""
        self.client.force_authenticate(user=self.user)
        res = self.client.get(exercise_url())

        exercises = Exercise.objects.all().order_by('id')
        serializer = ExerciseSerializer(exercises, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

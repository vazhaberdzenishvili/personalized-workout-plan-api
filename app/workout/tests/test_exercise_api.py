from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from core.models import Exercise, MuscleGroup
from workout.serializers import ExerciseSerializer


def exercise_url():
    """Return the exercise list URL"""
    return reverse('workout:exercise-list')


def detail_url(exercise_id):
    """Return the detail URL for a specific exercise"""
    return reverse('workout:exercise-detail', args=[exercise_id])


class ExerciseAPITest(APITestCase):
    """Test case for the Exercise API for normal user"""

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
            instructions="Lower hips to parallel, then stand"
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

    def test_user_cannot_create_exercise(self):
        """Test that a user cannot create an exercise"""
        self.client.force_authenticate(user=self.user)
        payload = {
            'name': 'Bench Press',
            'description': 'Targets chest and triceps',
            'target_muscles': [self.muscle_group.id]
        }
        res = self.client.post(exercise_url(), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_update_exercise(self):
        self.client.force_authenticate(user=self.user)
        """Test that a user cannot update an exercise"""
        payload = {'name': 'Modified Curl'}
        res = self.client.patch(detail_url(self.exercise.id), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete_exercise(self):
        self.client.force_authenticate(user=self.user)
        """Test that a user cannot delete an exercise"""
        res = self.client.delete(detail_url(self.exercise.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminExerciseAPITest(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email='admin@example.com', password='adminpass'
        )
        self.client.force_authenticate(user=self.admin)
        self.muscle_group = MuscleGroup.objects.create(
            name="Legs", description="Lower body muscles"
        )
        self.exercise = Exercise.objects.create(
            name="Squat",
            description="Strengthens legs and glutes",
            instructions="Lower hips to parallel, then stand"
        )
        self.exercise.target_muscles.add(self.muscle_group)

    def test_create_exercise(self):
        """Test that an admin can create an exercise"""
        payload = {
            'name': 'Deadlift',
            'description': 'Targets multiple muscle groups',
            'instructions': "Lower hips to parallel, then stand",
            'target_muscles': [self.muscle_group.id]
        }
        res = self.client.post(exercise_url(), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Exercise.objects.count(), 2)

    def test_retrieve_exercises(self):
        """Test that an admin can retrieve exercises"""
        res = self.client.get(exercise_url())
        exercises = Exercise.objects.all().order_by('id')
        serializer = ExerciseSerializer(exercises, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_exercise(self):
        """Test that an admin can update an exercise"""
        payload = {'name': 'Modified Curl'}
        res = self.client.patch(detail_url(self.exercise.id), payload)
        self.exercise.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.exercise.name, payload['name'])

    def test_delete_exercise(self):
        """Test that an admin can delete an exercise"""
        res = self.client.delete(detail_url(self.exercise.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Exercise.objects.filter(id=self.exercise.id).exists())

from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from core.models import MuscleGroup
from workout.serializers import MuscleGroupSerializer


def muscle_group_url():
    """Return the muscle group list URL"""
    return reverse('workout:muscle-group-list')


def detail_url(muscle_group_id):
    """Return the detail URL for a specific muscle group"""
    return reverse('workout:muscle-group-detail', args=[muscle_group_id])


class MuscleGroupAPITest(APITestCase):
    """Test case for the Muscle Group API for normal user"""

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

    def test_user_cannot_create_muscle_group(self):
        """Test that a user cannot create a muscle group"""
        self.client.force_authenticate(user=self.user)
        payload = {'name': 'Triceps', 'description': 'Back of the upper arm'}
        res = self.client.post(muscle_group_url(), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_update_muscle_group(self):
        """Test that a user cannot update a muscle group"""
        self.client.force_authenticate(user=self.user)
        payload = {'name': 'Modified Biceps'}
        res = self.client.patch(detail_url(self.muscle_group.id), payload)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_cannot_delete_muscle_group(self):
        self.client.force_authenticate(user=self.user)
        """Test that a user cannot delete a muscle group"""
        res = self.client.delete(detail_url(self.muscle_group.id))
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminMuscleGroupAPITest(APITestCase):
    """Test the muscle group API from an admin's perspective"""

    def setUp(self):
        self.client = APIClient()
        self.admin = get_user_model().objects.create_superuser(
            email='admin@example.com', password='adminpass'
        )
        self.client.force_authenticate(user=self.admin)
        self.muscle_group = MuscleGroup.objects.create(
            name="Arms", description="Includes biceps and triceps"
        )
        self.client.force_authenticate(user=self.admin)

    def test_create_muscle_group(self):
        """Test that an admin can create a muscle group"""
        payload = {'name': 'Forearms', 'description': 'Lower arm muscles'}
        res = self.client.post(muscle_group_url(), payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MuscleGroup.objects.count(), 2)

    def test_retrieve_muscle_groups(self):
        """Test that an admin can retrieve a list of muscle groups"""
        res = self.client.get(muscle_group_url())
        muscle_groups = MuscleGroup.objects.all().order_by('id')
        serializer = MuscleGroupSerializer(muscle_groups, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_muscle_group(self):
        """Test that an admin can update a muscle group"""
        payload = {'name': 'Upper Arms'}
        res = self.client.patch(detail_url(self.muscle_group.id), payload)
        self.muscle_group.refresh_from_db()
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.muscle_group.name, payload['name'])

    def test_delete_muscle_group(self):
        """Test that an admin can delete a muscle group"""
        res = self.client.delete(detail_url(self.muscle_group.id))
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(MuscleGroup.objects.filter(
            id=self.muscle_group.id).exists())

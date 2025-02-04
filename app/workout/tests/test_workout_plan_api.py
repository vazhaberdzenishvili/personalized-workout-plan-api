from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from core.models import WorkoutPlan
from workout.serializers import WorkoutPlanSerializer
from datetime import timedelta


def workout_plan_url():
    """Return the workout plan list URL"""
    return reverse('workout:workout-plan-list')


def detail_url(workout_plan_id):
    """Return the detail URL for a specific workout plan"""
    return reverse('workout:workout-plan-detail', args=[workout_plan_id])


def create_user(email='user@example.com', password='testpass123'):
    """Helper function to create a new user."""
    return get_user_model().objects.create_user(email, password)


def create_workout_plan(user, name="Full Body Strength"):
    """Helper function to create a workout plan."""
    return WorkoutPlan.objects.create(
        user=user,
        name=name,
        frequency=3,
        goal="Build muscle & strength",
        duration_per_session=timedelta(hours=1)
    )


class PublicWorkoutPlanApiTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test that authentication is required to access workout plans"""
        res = self.client.get(workout_plan_url())
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWorkoutPlanApiTests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_retrieve_workout_plans(self):
        """Test retrieving a list of workout plans"""
        create_workout_plan(user=self.user)
        create_workout_plan(user=self.user, name="Cardio Burn")

        res = self.client.get(workout_plan_url())

        workout_plans = WorkoutPlan.objects.filter(
            user=self.user).order_by('name')
        serializer = WorkoutPlanSerializer(workout_plans, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_workout_plans_limited_to_user(self):
        """Test that workout plans are limited to authenticated user"""
        other_user = create_user(email='other@example.com', password='test123')
        create_workout_plan(user=other_user)
        create_workout_plan(user=self.user)

        res = self.client.get(workout_plan_url())

        workout_plans = WorkoutPlan.objects.filter(user=self.user)
        serializer = WorkoutPlanSerializer(workout_plans, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_workout_plan_detail(self):
        """Test retrieving a single workout plan detail"""
        workout_plan = create_workout_plan(user=self.user)

        url = detail_url(workout_plan.id)
        res = self.client.get(url)

        serializer = WorkoutPlanSerializer(workout_plan)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_workout_plan_detail_unauthorized(self):
        """Test that a user cannot retrieve another user's workout plan"""
        other_user = create_user(
            email='other@example.com', password='testpass')
        workout_plan = create_workout_plan(user=other_user)

        url = detail_url(workout_plan.id)
        res = self.client.get(url)

        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_workout_plan(self):
        """Test creating a workout plan"""
        payload = {
            "name": "Leg Day",
            "frequency": 4,
            "goal": "Improve endurance",
            "duration_per_session": timedelta(minutes=45),
        }
        res = self.client.post(workout_plan_url(), payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        workout_plan = WorkoutPlan.objects.get(id=res.data['id'])
        for key, value in payload.items():
            self.assertEqual(getattr(workout_plan, key), value)
        self.assertEqual(workout_plan.user, self.user)

    def test_update_workout_plan(self):
        """Test updating a workout plan"""
        workout_plan = create_workout_plan(user=self.user)
        payload = {"name": "Upper Body", "frequency": 5}

        url = detail_url(workout_plan.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        workout_plan.refresh_from_db()
        self.assertEqual(workout_plan.name, payload["name"])
        self.assertEqual(workout_plan.frequency, payload["frequency"])

    def test_delete_workout_plan(self):
        """Test deleting a workout plan"""
        workout_plan = create_workout_plan(user=self.user)

        url = detail_url(workout_plan.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WorkoutPlan.objects.filter(
            id=workout_plan.id).exists())

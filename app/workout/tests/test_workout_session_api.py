from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from core.models import WorkoutPlan, WorkoutSession
from workout.serializers import WorkoutSessionSerializer
from datetime import date, timedelta


def workout_session_url():
    """Return the workout session list URL"""
    return reverse('workout:workout-session-list')


def detail_workout_session_url(workout_session_id):
    """Return the detail URL for a specific workout session"""
    return reverse('workout:workout-session-detail', args=[workout_session_id])


def create_user(email='user@example.com', password='testpass123'):
    """Helper function to create a new user."""
    return get_user_model().objects.create_user(email, password)


def create_workout_plan(user, name="Full Body Strength"):
    """Helper function to create a workout plan"""
    return WorkoutPlan.objects.create(
        user=user,
        name=name,
        frequency=3,
        goal="Build muscle & strength",
        duration_per_session=timedelta(hours=1)
    )


def create_workout_session(user, workout_plan):
    """Helper function to create a workout session"""
    return WorkoutSession.objects.create(
        user=user,
        workout_plan=workout_plan,
        date=date.today(),
        completed=False
    )


class PublicWorkoutSessionApiTests(TestCase):
    """Test unauthenticated API requests for workout sessions"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.workout_plan = create_workout_plan(user=self.user)

    def test_auth_required(self):
        """Test that authentication is required to access workout sessions"""
        res = self.client.get(workout_session_url())
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_workout_session(self):
        """Test that creating a workout session requires authentication"""
        payload = {
            "workout_plan": 1,
            "date": str(date.today()),
            "completed": False,
        }

        res = self.client.post(workout_session_url(), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_workout_session_detail(self):
        """Test retrieving workout session detail requires authentication"""
        workout_session = create_workout_session(self.user, self.workout_plan)

        url = detail_workout_session_url(workout_session.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWorkoutSessionApiTests(TestCase):
    """Test authenticated API requests for workout session"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.workout_plan = create_workout_plan(user=self.user)

    def test_create_workout_session(self):
        """Test creating a workout session is successful"""
        payload = {
            "workout_plan": self.workout_plan.id,
            "date": str(date.today()),
            "completed": False,
        }

        res = self.client.post(workout_session_url(), payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        workout_session = WorkoutSession.objects.get(id=res.data['id'])

        for key, value in payload.items():
            if key != 'workout_plan':
                if key == 'date':
                    self.assertEqual(str(getattr(workout_session, key)), value)
                else:
                    self.assertEqual(getattr(workout_session, key), value)
            else:
                self.assertEqual(workout_session.workout_plan.id, value)
        self.assertEqual(workout_session.workout_plan, self.workout_plan)

    def test_retrieve_workout_sessions(self):
        """Test retrieving a list of workout sessions"""
        create_workout_session(self.user, self.workout_plan)
        create_workout_session(self.user, self.workout_plan)

        res = self.client.get(workout_session_url())
        sessions = WorkoutSession.objects.filter(
            user=self.user).order_by('date')
        serializer = WorkoutSessionSerializer(sessions, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_workout_session_detail(self):
        """Test retrieving a single workout session detail"""
        workout_session = create_workout_session(self.user, self.workout_plan)

        url = detail_workout_session_url(workout_session.id)
        res = self.client.get(url)
        serializer = WorkoutSessionSerializer(workout_session)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_workout_session(self):
        """Test updating a workout session"""
        workout_session = create_workout_session(self.user, self.workout_plan)
        payload = {"completed": True}

        url = detail_workout_session_url(workout_session.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        workout_session.refresh_from_db()
        self.assertEqual(workout_session.completed, payload["completed"])

    def test_delete_workout_session(self):
        """Test deleting a workout session"""
        workout_session = create_workout_session(self.user, self.workout_plan)

        url = detail_workout_session_url(workout_session.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WorkoutSession.objects.filter(
            id=workout_session.id).exists())

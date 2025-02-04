from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from core.models import Progress
from workout.serializers import ProgressSerializer
from datetime import date, timedelta


def progress_url():
    """Return the progress list URL"""
    return reverse('workout:progress-list')


def detail_progress_url(progress_id):
    """Return the detail URL for a specific progress entry"""
    return reverse('workout:progress-detail', args=[progress_id])


def create_user(email='user@example.com', password='testpass123'):
    """Helper function to create a new user"""
    return get_user_model().objects.create_user(email, password)


def create_progress(user, weight=75.5, notes="Felt good", date=date.today()):
    """Helper function to create a Progress instance"""
    return Progress.objects.create(
        user=user, weight=weight, notes=notes, date=date
    )


class PublicProgressApiTests(TestCase):
    """Test unauthenticated API requests for progress"""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()

    def test_auth_required(self):
        """Test that authentication is required to access progress"""
        res = self.client.get(progress_url())
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_progress(self):
        """Test that creating a progress entry requires authentication"""
        payload = {
            "weight": 75.5,
            "notes": "Felt great after the workout",
            "date": str(date.today()),
        }

        res = self.client.post(progress_url(), payload, format='json')
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_retrieve_progress_detail(self):
        """Test progress detail retrieval requires auth"""
        progress = Progress.objects.create(
            user=self.user, weight=75.5, notes="Felt good", date=date.today()
        )

        url = detail_progress_url(progress.id)
        res = self.client.get(url)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateProgressApiTests(TestCase):
    """Test authenticated API requests for progress"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_create_progress(self):
        """Test creating a progress record"""
        payload = {
            "weight": 75.5,
            "notes": "Feeling strong after this workout",
            "date": str(date.today()),
        }

        res = self.client.post(progress_url(), payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        progress = Progress.objects.get(id=res.data['id'])

        for key, value in payload.items():
            if key == 'date':
                self.assertEqual(str(getattr(progress, key)), value)
            else:
                self.assertEqual(getattr(progress, key), value)

        self.assertEqual(progress.user, self.user)

    def test_retrieve_progresses(self):
        """Test retrieving a list of progress entries"""
        create_progress(self.user, weight=75.5,
                        notes="Felt good", date=date.today())
        create_progress(self.user, weight=76.0, notes="Great session",
                        date=date.today() + timedelta(days=1))

        res = self.client.get(progress_url())

        progresses = Progress.objects.filter(user=self.user).order_by('-date')
        serializer = ProgressSerializer(progresses, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_progress_detail(self):
        """Test retrieving a single progress entry detail"""
        progress = create_progress(
            self.user, weight=75.5, notes="Felt good", date=date.today())

        url = detail_progress_url(progress.id)
        res = self.client.get(url)

        serializer = ProgressSerializer(progress)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_update_progress(self):
        """Test updating a progress entry"""
        progress = create_progress(
            self.user, weight=75.5, notes="Felt good", date=date.today())

        payload = {"weight": 77.0, "notes": "Much stronger today!"}
        url = detail_progress_url(progress.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        progress.refresh_from_db()
        self.assertEqual(progress.weight, payload["weight"])
        self.assertEqual(progress.notes, payload["notes"])

    def test_delete_progress(self):
        """Test deleting a progress entry"""
        progress = create_progress(
            self.user, weight=75.5, notes="Felt good", date=date.today())

        url = detail_progress_url(progress.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Progress.objects.filter(id=progress.id).exists())

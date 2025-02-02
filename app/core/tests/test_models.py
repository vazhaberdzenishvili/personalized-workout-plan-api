"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


class ModelTests(TestCase):
    """Test models."""

    def test_create_user_with_email_successful(self):
        """Test creating a user with an email is successful."""
        email = 'test@example.com'
        password = 'testpass123'
        user = get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users."""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError."""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_superuser(self):
        """Test creating a superuser."""
        user = get_user_model().objects.create_superuser(
            'test@example.com',
            'test123',
        )
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_create_muscle_group(self):
        """Test creating a muscle group"""
        target_muscles = models.MuscleGroup.objects.create(
            name="Biceps",
            description="Muscles in the upper arm, responsible for arm flexion"
        )
        self.assertEqual(str(target_muscles), target_muscles.name)

    def test_create_exercise_with_muscle_groups(self):
        """Test creating an exercise with associated muscle groups"""
        muscle_group = models.MuscleGroup.objects.create(
            name="Biceps",
            description="Muscles in the upper arm, responsible for arm flexion"
        )
        exercise = models.Exercise.objects.create(
            name="Bicep Curls",
            description="An exercise to strengthen the biceps",
            instructions="Curl arms while holding weights"
        )
        exercise.target_muscles.add(muscle_group)
        self.assertEqual(str(exercise), exercise.name)
        self.assertIn(muscle_group, exercise.target_muscles.all())

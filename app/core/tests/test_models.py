"""
Tests for models.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from core import models


def create_user(email='user@example.com', password='testpass123'):
    """Create and return a new user."""
    return get_user_model().objects.create_user(email, password)


def create_exercise(name='Biceps',
                    description="Muscles in the upper arm",
                    instructions="Curl arms while holding weights"):
    """Create and return a new exercise."""
    return models.Exercise.objects.create(
        name=name,
        description=description,
        instructions=instructions
    )


class ModelTests(TestCase):
    """Test models."""

    def setUp(self):
        """Set up for tests."""
        self.user = create_user()

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

    def test_create_workout_plan(self):
        """Test creating a workout plan"""
        workout_plan = models.WorkoutPlan.objects.create(
            user=self.user,
            name='Full Body Strength',
            frequency=3,
            goal='Build muscle & strength',
            duration_per_session="01:00:00"
        )

        self.assertEqual(
            str(workout_plan),
            f"{workout_plan.name} ({workout_plan.frequency}/week)"
        )

    def test_create_workout_plan_exercise(self):
        """Test creating a workout plan exercise"""
        workout_plan = models.WorkoutPlan.objects.create(
            user=self.user,
            name='Full Body Strength',
            frequency=3,
            goal='Build muscle & strength',
            duration_per_session="01:00:00"
        )
        exercise = models.Exercise.objects.create(
            name="Push-up",
            description="A basic push-up exercise"
        )

        workout_plan_exercise = models.WorkoutPlanExercise.objects.create(
            workout_plan=workout_plan,
            exercise=exercise,
            repetitions=12,
            sets=4,
            duration="00:45:00",
            distance=5.2
        )

        self.assertEqual(
            str(workout_plan_exercise),
            f"{exercise.name} ({workout_plan_exercise.repetitions} reps, "
            f"{workout_plan_exercise.sets} sets) in {workout_plan.name}"
        )

    def test_create_workout_session(self):
        """Test creating a workout session"""
        workout_plan = models.WorkoutPlan.objects.create(
            user=self.user,
            name='Full Body Strength',
            frequency=3,
            goal='Build muscle & strength',
            duration_per_session="01:00:00"
        )

        workout_session = models.WorkoutSession.objects.create(
            user=self.user,
            workout_plan=workout_plan,
            date="2025-02-03",
            completed=True
        )

        self.assertEqual(
            str(workout_session),
            f"{self.user.name} - {workout_session.workout_plan.name} "
            f"({workout_session.date})"
        )

    def test_create_progress(self):
        """Test creating a progress record"""
        progress = models.Progress.objects.create(
            user=self.user,
            date="2025-02-03",
            weight=70.5,
            notes="Feeling good!"
        )

        self.assertEqual(
            str(progress),
            f"Progress of {self.user.name} on {progress.date}"
        )

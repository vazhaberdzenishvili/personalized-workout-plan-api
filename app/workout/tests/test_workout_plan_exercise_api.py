from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APIClient
from core.models import WorkoutPlan, WorkoutPlanExercise, Exercise
from workout.serializers import WorkoutPlanExerciseSerializer
from datetime import timedelta


def workout_plan_exercise_url():
    """Return the workout plan exercise list URL"""
    return reverse('workout:workout-plan-exercise-list')


def detail_workout_plan_exercise_url(workout_plan_exercise_id):
    """Return the detail URL for a specific workout plan exercise"""
    return reverse(
        'workout:workout-plan-exercise-detail',
        args=[workout_plan_exercise_id]
    )


def create_user(email='user@example.com', password='testpass123'):
    """Helper function to create a new user"""
    return get_user_model().objects.create_user(email, password)


def create_workout_plan_exercise(
    workout_plan, exercise, repetitions=10, sets=3
):
    """Helper function to create a workout plan exercise"""
    return WorkoutPlanExercise.objects.create(
        workout_plan=workout_plan,
        exercise=exercise,
        repetitions=repetitions,
        sets=sets
    )


def create_workout_plan(user, name="Full Body Strength"):
    """Helper function to create a workout plan"""
    return WorkoutPlan.objects.create(
        user=user,
        name=name,
        frequency=3,
        goal="Build muscle & strength",
        duration_per_session=timedelta(hours=1)
    )


class PublicWorkoutPlanExerciseApiTests(TestCase):
    """Test unauthenticated API requests"""

    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        """Test authentication required for workout plan exercises"""
        res = self.client.get(workout_plan_exercise_url())
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateWorkoutPlanExerciseApiTests(TestCase):
    """Test authenticated API requests"""

    def setUp(self):
        self.user = create_user()
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.workout_plan = create_workout_plan(user=self.user)
        self.exercise = Exercise.objects.create(
            name="Push-Up", description="A basic push-up exercise")

    def test_retrieve_workout_plan_exercises(self):
        """Test retrieving a list of workout plan exercises"""
        workout_plan = create_workout_plan(user=self.user)
        exercise = Exercise.objects.create(
            name="Sample Exercise", description="Sample description")
        create_workout_plan_exercise(
            workout_plan=workout_plan, exercise=exercise)

        res = self.client.get(workout_plan_exercise_url())

        exercises = WorkoutPlanExercise.objects.filter(
            workout_plan=workout_plan).order_by('id')
        serializer = WorkoutPlanExerciseSerializer(exercises, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_workout_plan_exercises_limited_to_user(self):
        """Test workout plan exercises limited to authenticated user's plans"""
        other_user = create_user(email='other@example.com', password='test123')
        other_workout_plan = create_workout_plan(user=other_user)
        create_workout_plan_exercise(
            workout_plan=other_workout_plan, exercise=self.exercise)
        create_workout_plan_exercise(
            workout_plan=self.workout_plan, exercise=self.exercise)

        res = self.client.get(workout_plan_exercise_url())

        workout_plan_exercises = WorkoutPlanExercise.objects.filter(
            workout_plan=self.workout_plan)
        serializer = WorkoutPlanExerciseSerializer(
            workout_plan_exercises, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_workout_plan_exercise_detail(self):
        """Test retrieving a single workout plan exercise detail"""
        workout_plan_exercise = create_workout_plan_exercise(
            workout_plan=self.workout_plan, exercise=self.exercise)

        url = detail_workout_plan_exercise_url(workout_plan_exercise.id)
        res = self.client.get(url)

        serializer = WorkoutPlanExerciseSerializer(workout_plan_exercise)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_workout_plan_exercise(self):
        """Test creating a workout plan exercise"""
        exercise = Exercise.objects.create(
            name="Push-ups",
            description="Upper body strength exercise"
        )
        workout_plan = create_workout_plan(user=self.user)
        payload = {
            "workout_plan": workout_plan.id,
            "exercise": exercise.id,
            "repetitions": 10,
            "sets": 3,
        }

        res = self.client.post(
            workout_plan_exercise_url(), payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        workout_plan_exercise = WorkoutPlanExercise.objects.get(
            id=res.data['id'])

        for k, v in payload.items():
            if k == 'exercise':
                self.assertEqual(getattr(workout_plan_exercise, k).id, v)
            elif k != 'workout_plan':
                self.assertEqual(getattr(workout_plan_exercise, k), v)

        self.assertEqual(workout_plan_exercise.workout_plan, workout_plan)

    def test_update_workout_plan_exercise(self):
        """Test updating a workout plan exercise"""
        workout_plan_exercise = create_workout_plan_exercise(
            workout_plan=self.workout_plan, exercise=self.exercise)
        payload = {"repetitions": 15, "sets": 4}

        url = detail_workout_plan_exercise_url(workout_plan_exercise.id)
        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        workout_plan_exercise.refresh_from_db()
        self.assertEqual(workout_plan_exercise.repetitions,
                         payload["repetitions"])
        self.assertEqual(workout_plan_exercise.sets, payload["sets"])

    def test_delete_workout_plan_exercise(self):
        """Test deleting a workout plan exercise"""
        workout_plan_exercise = create_workout_plan_exercise(
            workout_plan=self.workout_plan, exercise=self.exercise)

        url = detail_workout_plan_exercise_url(workout_plan_exercise.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(WorkoutPlanExercise.objects.filter(
            id=workout_plan_exercise.id).exists())

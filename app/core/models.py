"""
Database models.
"""
from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.utils import timezone


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return a new user."""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """Create and return a new superuser."""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class MuscleGroup(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class Exercise(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    instructions = models.TextField()
    target_muscles = models.ManyToManyField(MuscleGroup)

    def __str__(self):
        return self.name


class WorkoutPlan(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="workout_plans"
    )
    name = models.CharField(max_length=255)
    frequency = models.PositiveIntegerField(
        help_text="The frequency of the workout plan"
        "(e.g., 3 for 3 times a week)"
    )
    goal = models.CharField(max_length=255)
    duration_per_session = models.DurationField(
        null=True, blank=True,
        help_text="Duration of each session"
    )

    def __str__(self):
        return f"{self.name} ({self.frequency}/week)"


class WorkoutPlanExercise(models.Model):
    workout_plan = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.CASCADE,
        related_name='workout_plan_exercises'
    )
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    repetitions = models.PositiveIntegerField(blank=True, default=1)
    sets = models.PositiveIntegerField(blank=True, default=1)
    duration = models.DurationField(
        null=True, blank=True,
        help_text="Duration (e.g., 1 hour, 30 minutes)"
    )
    distance = models.FloatField(null=True, blank=True)

    def __str__(self):
        return (
            f"{self.exercise.name} ({self.repetitions} reps, "
            f"{self.sets} sets) in {self.workout_plan.name}"
        )


class WorkoutSession(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="workout_sessions"
    )
    workout_plan = models.ForeignKey(
        WorkoutPlan, on_delete=models.CASCADE, related_name="sessions"
    )
    date = models.DateField()
    completed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.name} - {self.workout_plan.name} ({self.date})"


class Progress(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="progress"
    )
    date = models.DateField(default=timezone.now)
    weight = models.FloatField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'date')

    def __str__(self):
        return f"Progress of {self.user.name} on {self.date}"

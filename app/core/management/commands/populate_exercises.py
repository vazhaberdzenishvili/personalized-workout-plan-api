from django.core.management.base import BaseCommand
from core.models import Exercise, MuscleGroup


class Command(BaseCommand):
    help = (
        'Resets and seeds the DB with predefined exercises and '
        'target muscles.'
    )

    def handle(self, *args, **kwargs):

        # Clear existing data
        Exercise.objects.all().delete()
        MuscleGroup.objects.all().delete()
        self.stdout.write(self.style.SUCCESS(
            'Existing data cleared successfully!'))

        target_muscles = [
            {"name": "Chest", "description": "Muscles of the chest"},
            {"name": "Back", "description": "Muscles of the back"},
            {"name": "Arms", "description": "Muscles of the arms"},
            {"name": "Shoulders", "description": "Muscles of the shoulders"},
            {"name": "Legs", "description": "Muscles of the lower body"},
            {"name": "Glutes", "description": "Muscles of the buttocks"},
            {"name": "Core", "description": "Abs and lower back"},
            {"name": "Traps", "description": "Upper back trapezius muscles"},
            {"name": "Calves", "description": "Lower leg muscles"},
            {"name": "Forearms", "description": "Forearm and wrist muscles"},
        ]

        for muscle_data in target_muscles:
            MuscleGroup.objects.get_or_create(
                name=muscle_data["name"],
                defaults={"description": muscle_data["description"]}
            )
        self.stdout.write(self.style.SUCCESS(
            'Target muscles populated successfully!'))

        exercises = [
            {"name": "Push-up", "description": (
                "Bodyweight exercise for chest, shoulders, and triceps"
            ), "target_muscles": ["Chest", "Shoulders", "Arms"]},
            {"name": "Squat", "description": (
                "Lower-body exercise for thighs, hips, and buttocks"
            ), "target_muscles": ["Legs", "Glutes", "Core"]},
            {"name": "Deadlift", "description": (
                "A weightlifting exercise for the back, glutes, and legs."
            ), "target_muscles": ["Back", "Legs", "Glutes"]},
            {"name": "Bench Press", "description": (
                "A chest exercise that also targets shoulders and triceps."
            ), "target_muscles": ["Chest", "Shoulders", "Arms"]},
            {"name": "Pull-up", "description": (
                "Upper-body exercise for back and biceps."
            ), "target_muscles": ["Back", "Arms"]},
            {"name": "Overhead Press", "description": (
                "Shoulder exercise for triceps and upper chest."
            ), "target_muscles": ["Shoulders", "Arms"]},
            {"name": "Lunge", "description": (
                "Lower-body exercise for legs and glutes."
            ), "target_muscles": ["Legs", "Glutes"]},
            {"name": "Leg Press", "description": (
                "A machine-based exercise that targets the legs and glutes."
            ), "target_muscles": ["Legs", "Glutes"]},
            {"name": "Bicep Curl", "description": (
                "An exercise focusing on the biceps.",
            ), "target_muscles": ["Arms"]},
            {"name": "Tricep Dip", "description": (
                "An exercise targeting the triceps using bodyweight."
            ), "target_muscles": ["Arms"]},
            {"name": "Lat Pulldown", "description": (
                "A back exercise that also engages the biceps and shoulders."
            ), "target_muscles": ["Back", "Arms"]},
            {"name": "Romanian Deadlift", "description": (
                "A hamstring-focused deadlift variation."
            ), "target_muscles": ["Legs", "Glutes"]},
            {"name": "Plank", "description": (
                "Core exercise for abs and lower back."
            ), "target_muscles": ["Core"]},
            {"name": "Russian Twist", "description": (
                "Rotational core exercise.",
            ), "target_muscles": ["Core"]},
            {"name": "Mountain Climbers", "description": (
                "A full-body workout that engages the core and legs."
            ), "target_muscles": ["Core", "Legs"]},
            {"name": "Dumbbell Rows", "description": (
                "A back exercise that targets the upper back and biceps."
            ), "target_muscles": ["Back", "Arms"]},
            {"name": "Chest Fly", "description": (
                "A chest exercise using dumbbells or cables.",
            ), "target_muscles": ["Chest"]},
            {"name": "Calf Raise", "description": "Calf exercise.",
             "target_muscles": ["Calves"]},
            {"name": "Forearm Curl", "description": (
                "An exercise that targets the forearms and wrist flexors."
            ), "target_muscles": ["Forearms"]},
            {"name": "Tricep Pushdown", "description": (
                "Tricep exercise with a cable machine."
            ), "target_muscles": ["Arms"]}
        ]

        for exercise_data in exercises:
            exercise, created = Exercise.objects.get_or_create(
                name=exercise_data["name"],
                description=exercise_data["description"]
            )

            target_muscles = MuscleGroup.objects.filter(
                name__in=exercise_data["target_muscles"])
            exercise.target_muscles.set(target_muscles)

            if created:
                self.stdout.write(self.style.SUCCESS(
                    f'Exercise "{exercise.name}" created successfully.'))
            else:
                self.stdout.write(self.style.SUCCESS(
                    f'Exercise "{exercise.name}" already exists.'))

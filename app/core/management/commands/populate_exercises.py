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
            {
                "name": "Push-up",
                "description": "Chest, shoulders, triceps exercise",
                "instruction": "Lower and push up body",
                "target_muscles": ["Chest", "Shoulders", "Arms"]
            },
            {
                "name": "Squat",
                "description": "exercise for thighs, hips, and buttocks",
                "instruction": "Lower hips, then stand",
                "target_muscles": ["Legs", "Glutes", "Core"]
            },
            {
                "name": "Deadlift",
                "description": "exercise for the back, glutes, and legs",
                "instruction": "Lift bar, then lower",
                "target_muscles": ["Back", "Legs", "Glutes"]
            },
            {
                "name": "Bench Press",
                "description": "exercise that targets shoulders and triceps",
                "instruction": "Press bar up and down",
                "target_muscles": ["Chest", "Shoulders", "Arms"]
            },
            {
                "name": "Pull-up",
                "description": "Upper-body exercise for back and biceps",
                "instruction": "Pull up body",
                "target_muscles": ["Back", "Arms"]
            },
            {
                "name": "Overhead Press",
                "description": "Shoulder exercise for triceps and upper chest",
                "instruction": "Press weights overhead",
                "target_muscles": ["Shoulders", "Arms"]
            },
            {
                "name": "Lunge",
                "description": "Lower-body exercise for legs and glutes",
                "instruction": "Step forward, lower body",
                "target_muscles": ["Legs", "Glutes"]
            },
            {
                "name": "Leg Press",
                "description": "exercise targets the legs and glutes",
                "instruction": "Press platform with legs",
                "target_muscles": ["Legs", "Glutes"]
            },
            {
                "name": "Bicep Curl",
                "description": "An exercise focusing on the biceps",
                "instruction": "Curl weights up",
                "target_muscles": ["Arms"]
            },
            {
                "name": "Tricep Dip",
                "description": "exercise targets triceps using bodyweight",
                "instruction": "Dip body, then lift",
                "target_muscles": ["Arms"]
            },
            {
                "name": "Lat Pulldown",
                "description": "A back exercise for biceps and shoulders",
                "instruction": "Pull bar down to chest",
                "target_muscles": ["Back", "Arms"]
            },
            {
                "name": "Romanian Deadlift",
                "description": "A hamstring-focused deadlift variation",
                "instruction": "Lower bar to shin, then stand",
                "target_muscles": ["Legs", "Glutes"]
            },
            {
                "name": "Plank",
                "description": "Core exercise for abs and lower back",
                "instruction": "Hold body in line",
                "target_muscles": ["Core"]
            },
            {
                "name": "Russian Twist",
                "description": "Rotational core exercise",
                "instruction": "Twist torso side to side",
                "target_muscles": ["Core"]
            },
            {
                "name": "Mountain Climbers",
                "description": "A full-body workout for the core and legs",
                "instruction": "Run in place on hands",
                "target_muscles": ["Core", "Legs"]
            },
            {
                "name": "Dumbbell Rows",
                "description": "A back exercise for upper back and biceps",
                "instruction": "Row weights to waist",
                "target_muscles": ["Back", "Arms"]
            },
            {
                "name": "Chest Fly",
                "description": "A chest exercise using dumbbells or cables",
                "instruction": "Open and close arms",
                "target_muscles": ["Chest"]
            },
            {
                "name": "Calf Raise",
                "description": "Calf exercise",
                "instruction": "Raise and lower heels",
                "target_muscles": ["Calves"]
            },
            {
                "name": "Forearm Curl",
                "description": "An exercise for forearms and wrist flexors",
                "instruction": "Curl weights up",
                "target_muscles": ["Forearms"]
            },
            {
                "name": "Tricep Pushdown",
                "description": "Tricep exercise with a cable machine",
                "instruction": "Push bar down",
                "target_muscles": ["Arms"]
            }
        ]

        for exercise_data in exercises:
            exercise, created = Exercise.objects.get_or_create(
                name=exercise_data["name"],
                description=exercise_data["description"],
                instructions=exercise_data["instruction"]
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

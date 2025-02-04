# Personalized Workout Plan API

## Introduction

The Personalized Workout Plan API is a RESTful platform that enables users to create and manage custom workout plans, while tracking their fitness progress. With secure user authentication, a wide range of predefined exercises, and detailed progress tracking, it streamlines the process of reaching fitness goals.

## Features

- **User Authentication**: Secure registration and login system for managing personal workout plans.

- **Predefined Exercises Database**: A collection of 20 predefined exercises with descriptions, instructions, and target muscles.

- **Personalized Workout Plans**: Users can create personalized plans by selecting exercises from the database and customizing sets, reps, duration, or distance based on their goals.

- **Tracking and Goals**: Users can track weight over time and set fitness goals, including weight targets and exercise-specific achievements.

## Tech Stack

- **Python**: The Core programming language.

- **Django**: Web framework for building the API.

- **PostgreSQL**: Database management system for storing workout plans and user data.

- **JWT**: JSON Web Tokens for secure API authentication.

- **Swagger**: Tool for generating interactive API documentation.

- **Docker**: Platform for containerized development and deployment.


## Installation

Follow these steps to set up the Personalized Workout plan API locally, including installing dependencies and configuring the environment.

### Prerequisites

Before you begin, ensure you have the following installed:

- **Docker** and **Docker Compose**


### Steps:

1. **Clone the repository:**

   ```sh
   git clone https://github.com/vazhaberdzenishvili/personalized-workout-plan-api.git
   ```
2. **Build and start the Docker containers:**

   ```sh
   docker compose up --build
   ```

## Admin Setup

To manage workout plans and user data through the admin panel, you'll need to create a superuser. Make sure the Docker containers are running before proceeding.

Run the following command inside the Docker container:.

   ```sh
        docker compose run --rm app sh -c "python manage.py createsuperuser"
   ```
   Follow the prompts to set up your admin email and password.


## Populating the Predefined Exercises Database
To get started with a predefined set of exercises, populate the database with at least 20 diverse exercises using the provided custom command. This ensures users have a variety of exercises available for creating personalized workout plans.

-   ### Command to Populate the Database
    Run the following command to populate the Predefined Exercises:

    ```sh
        docker compose run --rm app sh -c "python manage.py populate_exercises"
    ```
    **Note:** This command will populate your database with a set of 20 diverse predefined exercises, making them available for use in creating personalized workout plans.

## Usage

### User Registration and Authentication

The Personalized Workout Plan API uses **JWT (JSON Web Token)** for authentication. Users can obtain a token by logging in, which is then used to authorize access to protected endpoints.

- #### User Registration
    To register a new user and access the API, send a POST request to `/api/user/create/` with the following example JSON payload:
    ```json
    {
        "email": "user@example.com",
        "password": "password123",
        "name": "User name"
    }
    ```
    **Note:** Replace the values with your own credentials when registering.

- #### Obtain a token for authentication.
    After registering, send a POST request to `/api/user/token/` with the user's credentials to obtain an access token and a refresh token:

    **Example Request:**
    ```json
     {
        "email": "user@example.com",
        "password": "password123"
     }
    ```

    **Example Response:**
    ```json
     {
        "refresh": "refresh_token",
        "access": "access_token"
     }
    ```

- #### Authenticate and Access Protected Endpoints
    Use the access token to authenticate and access protected endpoints by including it in the Authorization header. **Only the token** itself is needed—do not include any prefixes like 'Bearer' or 'Token'."

- #### Access Token Expiry and Refresh
    The access token has a short lifetime and will expire after a certain period. To obtain a new access token, you can use the refresh token by sending a POST request to `/api/user/token/refresh/`.

    **Example Request:**
    ```json
    {
        "refresh": "refresh_token"
    }
    ```

## Exercise & Muscle Group APIs
The **Exercise** and **Muscle Group APIs** allow users to retrieve predefined exercises and muscle groups. **Only admin** users can create, update, or delete them, while regular users have read-only access.

- ### Retrieve Exercises
    - GET `/api/workout/exercises/`

    **Example Response:**
    ```json
    {
        "id": 1,
        "name": "Push-up",
        "description": "Chest, shoulders, triceps exercise",
        "instructions": "Lower and push up body",
        "target_muscle_names": [
            "Chest",
            "Arms",
            "Shoulders"
        ]
    }
    ```
- ### Retrieve Muscle Groups
    - GET `/api/workout/muscle_groups/`

    **Example Response:**
    ```json
    {
        "id": 1,
        "name": "Chest",
        "description": "Muscles of the chest"
    }
    ```
## Workout Plan API
The Workout Plan API enables users to **create, read, update, and delete** workout plans. As mentioned earlier, **authorization** is required for these operations.

-   #### Create Workout Plan:

    - **POST** `/api/workout/workout_plan/`

        **Example payload to create a new workout plan:**

        ```json
        {
            "name": "Full Body Strength",
            "frequency": 3,
            "goal": "Build muscle & strength",
            "duration_per_session": "01:00:00"
        }
        ```

## Workout Plan Exercise API
The Workout Plan Exercise API allows you to **assign, retrieve, update, and remove** exercises from a workout plan. **Authorization** is required to perform these actions.

-   #### Create Workout Plan Exercise:

    - **POST** `/api/workout/workout_plan_exercise/`

        **Example payload to assign an exercise to a workout plan:**

        ```json
        {
            "repetitions": 12,
            "sets": 4,
            "duration": "00:45:00",
            "distance": 5.2,
            "workout_plan": 1,
            "exercise": 3
        }
        ```
## Workout Session API
The Workout Session API allows users to **log, track, and manage their workout sessions.**. **Authorization** is required to perform these actions.

-   #### Log a Workout Session:

    - **POST** `/api/workout/workout_session/`

        **Example payload to create a new workout session:**

        ```json
        {
            "workout_plan": 1,
            "date": "2025-01-01",
            "completed": false
        }
        ```


## Progress Tracking API
The Progress Tracking API allows users to **log and monitor** their fitness progress over time. Authorization is required to perform these actions.

-   #### Log Progress Entry:

    - **POST** `/api/workout/progress/`

        **Example payload to log a progress entry:**

        ```json
        {
            "date": "2025-02-04",
            "weight": 0,
            "notes": "string"
        }
        ```

## API Documentation

The Personalized Workout Plan API includes Swagger, an interactive interface for exploring and testing all available endpoints. It provides a user-friendly way to understand the API structure and functionality.

### Accessing the Documentation

Once the server is running, open your browser and navigate to:

```bash
http://localhost:8000/api/docs/
```
## Testing

The test suite ensures that all features work as intended, offering reliability and confidence in your deployment. To run the tests, use the following command:

```sh
   docker compose run --rm app sh -c "python manage.py test"
```

## Linting

To ensure high code quality and maintain consistency, the project utilizes Flake8 for linting. It checks for syntax errors, unused imports, and PEP 8 compliance.

Run the following command to inspect the codebase:

```sh
   docker compose run --rm app sh -c "flake8"
```

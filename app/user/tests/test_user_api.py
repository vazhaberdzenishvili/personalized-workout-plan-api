"""
Tests for the user API.
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


CREATE_USER_URL = reverse('user:create')
TOKEN_URL = reverse('user:token_obtain_pair')
TOKEN_REFRESH_URL = reverse('user:token_refresh')
LOGOUT_URL = reverse('user:logout')
ME_URL = reverse('user:me')


def create_user(**params):
    """Create and return a new user."""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API."""

    def setUp(self):
        self.client = APIClient()
        self.user_details = {
            'name': 'Test Name',
            'email': 'test1@example.com',
            'password': 'testpass123',
        }
        self.user = get_user_model().objects.create_user(**self.user_details)

    def test_create_user_success(self):
        """Test creating a user is successful."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))
        self.assertNotIn('password', res.data)

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists."""
        payload = {
            'email': 'test@example.com',
            'password': 'testpass123',
            'name': 'Test Name',
        }
        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        """Test an error is returned if password less than 5 chars."""
        payload = {
            'email': 'test@example.com',
            'password': 'pw',
            'name': 'Test name',
        }
        res = self.client.post(CREATE_USER_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        user_exists = get_user_model().objects.filter(
            email=payload['email']
        ).exists()
        self.assertFalse(user_exists)

    def test_create_token_for_user(self):
        """Test JWT token is generated for valid credentials."""
        payload = {
            'email': self.user.email,
            'password': self.user_details['password'],
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_create_token_bad_credentials(self):
        """Test returns error if credentials are invalid."""
        payload = {
            'email': self.user.email,
            'password': 'wrongpass',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_email_not_found(self):
        """Test error returned if user does not exist."""
        payload = {
            'email': 'unknown@example.com',
            'password': 'pass123',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_token_blank_password(self):
        """Test posting a blank password returns an error."""
        payload = {
            'email': self.user.email,
            'password': '',
        }
        res = self.client.post(TOKEN_URL, payload)

        self.assertNotIn('access', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthorized(self):
        """Test authentication is required for users."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Test API requests that require authentication."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='test@example.com',
            password='testpass123',
            name='Test Name',
        )
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_retrieve_profile_success(self):
        """Test retrieving profile for logged in user."""
        res = self.client.get(ME_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {
            'name': self.user.name,
            'email': self.user.email,
        })

    def test_post_me_not_allowed(self):
        """Test POST is not allowed for the me endpoint."""
        res = self.client.post(ME_URL, {})

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_user_profile(self):
        """Test updating the user profile for the authenticated user."""
        payload = {'name': 'Updated name', 'password': 'updatedpass123'}
        res = self.client.patch(ME_URL, payload)
        self.user.refresh_from_db()

        self.assertEqual(self.user.name, payload['name'])
        self.assertTrue(self.user.check_password(payload['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)


class LogoutTests(TestCase):
    """Test JWT logout functionality."""

    def setUp(self):
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='pass123',
            name='User',
        )
        self.client = APIClient()
        self.tokens = self.get_tokens()

    def get_tokens(self):
        """Generate access and refresh tokens for the user."""
        refresh = RefreshToken.for_user(self.user)
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }

    def test_logout_invalidates_refresh_token(self):
        """Ensure refresh token is invalidated after logout."""
        refresh_token = self.tokens["refresh"]

        res = self.client.post(
            LOGOUT_URL, {"refresh_token": refresh_token}, format="json")
        self.assertEqual(res.status_code, status.HTTP_200_OK)

        res = self.client.post(TOKEN_REFRESH_URL, {
                               "refresh": refresh_token}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Token is blacklisted", res.data["detail"])

    def test_access_token_still_valid_if_not_blacklisted(self):
        """Ensure access token is still valid after logout"""
        access_token = self.tokens["access"]
        refresh_token = self.tokens["refresh"]

        self.client.post(
            LOGOUT_URL, {"refresh_token": refresh_token}, format="json")

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {access_token}")
        res = self.client.get(ME_URL)
        self.assertNotEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_requires_refresh_token(self):
        """Ensure logout request fails if refresh token is not provided."""
        res = self.client.post(LOGOUT_URL, {}, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("refresh_token", res.data)

    def test_logout_with_invalid_refresh_token(self):
        """Ensure logout fails when an invalid refresh token is provided."""
        res = self.client.post(
            LOGOUT_URL, {"refresh_token": "invalidtoken"}, format="json")
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("Token is invalid or expired", res.data["error"])

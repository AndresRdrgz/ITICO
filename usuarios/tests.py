from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from .models import UserProfile


class UserProfileModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_user_profile_creation(self):
        """Test that UserProfile is automatically created when User is created"""
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)

    def test_get_display_name(self):
        """Test get_display_name method"""
        # Test with full name
        self.user.first_name = 'John'
        self.user.last_name = 'Doe'
        self.user.save()
        self.assertEqual(self.user.profile.get_display_name(), 'John Doe')

        # Test with only username
        self.user.first_name = ''
        self.user.last_name = ''
        self.user.save()
        self.assertEqual(self.user.profile.get_display_name(), 'testuser')

    def test_get_profile_picture_url(self):
        """Test get_profile_picture_url method"""
        # Test without profile picture
        self.assertEqual(
            self.user.profile.get_profile_picture_url(),
            '/static/images/default-avatar.svg'
        )


class UserProfileViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )

    def test_profile_edit_view_requires_login(self):
        """Test that profile edit view requires login"""
        response = self.client.get(reverse('usuarios:profile_edit'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_profile_edit_view_with_login(self):
        """Test profile edit view with authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('usuarios:profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/profile_edit.html')

    def test_change_password_view_requires_login(self):
        """Test that change password view requires login"""
        response = self.client.get(reverse('usuarios:change_password'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_change_password_view_with_login(self):
        """Test change password view with authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('usuarios:change_password'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/change_password.html')

    def test_profile_view_requires_login(self):
        """Test that profile view requires login"""
        response = self.client.get(reverse('usuarios:profile_view'))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_profile_view_with_login(self):
        """Test profile view with authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('usuarios:profile_view'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'usuarios/profile_view.html')

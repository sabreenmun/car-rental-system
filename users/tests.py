from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from designpatterns.sessionmanager import SessionManager
CustomUser = get_user_model()  # Get the swapped user model

class UserLoginTestCase(TestCase):
    def setUp(self):
        """Create test users"""
        self.client = Client()
        self.renter = CustomUser.objects.create_user(username='renter1', password='renterpass')
        self.owner = CustomUser.objects.create_superuser(username='owner1', password='ownerpass')

    def test_singleton_instance(self):
        """Ensure SessionManager follows Singleton pattern"""
        instance1 = SessionManager()
        instance2 = SessionManager()
        self.assertIs(instance1, instance2)  # Both instances should be the same

    def test_renter_login(self):
        """Test successful login for renter"""
        response = self.client.post(reverse('car_renter_login'), {
            'username': 'renter1',
            'password': 'renterpass'
        })
        self.assertEqual(response.status_code, 302)  # Expecting redirect on success
        self.assertTrue('_auth_user_id' in self.client.session)  # Session should be set

    def test_owner_login(self):
        """Test successful login for owner"""
        response = self.client.post(reverse('car_owner_login'), {
            'username': 'owner1',
            'password': 'ownerpass'
        })
        self.assertEqual(response.status_code, 302)  # Expecting redirect on success
        self.assertTrue('_auth_user_id' in self.client.session)  # Session should be set

    def test_invalid_login(self):
        """Test login failure with incorrect credentials"""
        response = self.client.post(reverse('car_renter_login'), {
            'username': 'wronguser',
            'password': 'wrongpass'
        })
        self.assertEqual(response.status_code, 200)  # Page should reload
        self.assertFalse('_auth_user_id' in self.client.session)  # No session should be set

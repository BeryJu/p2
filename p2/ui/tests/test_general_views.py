"""p2 ui General View tests"""
from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase


class GeneralViewTests(TestCase):
    """Test general views"""

    def setUp(self):
        self.user, _ = User.objects.get_or_create(
            username='p2-unittest')
        self.client.force_login(self.user)

    def test_general_index_view(self):
        """Test index view (authenticated)"""
        response = self.client.get(reverse('p2_ui:index'))
        self.assertEqual(response.status_code, 200)

"""p2 public access compoennt tests"""
from django.test import TestCase
from guardian.shortcuts import get_anonymous_user

from p2.components.public_access.controller import PublicAccessController
from p2.core.models import Blob, Component, Volume
from p2.core.tests.utils import get_test_storage
from p2.lib.reflection import class_to_path


class TestPublicAccess(TestCase):
    """p2 public access compoennt tests"""

    def setUp(self):
        self.storage = get_test_storage()
        self.volume = Volume.objects.create(
            name='p2-unittest-public-access',
            storage=self.storage)
        self.component = Component.objects.create(
            volume=self.volume,
            controller_path=class_to_path(PublicAccessController))

    def test_add_permissions(self):
        """Create blob and check that anonymous user gets view permission assigned"""
        _blob = Blob.objects.create(
            path='/test',
            volume=self.volume)
        # Reload from DB so we get the latest data
        blob = Blob.objects.get(pk=_blob.pk)
        self.assertTrue(get_anonymous_user().has_perm('p2_core.view_blob', blob))

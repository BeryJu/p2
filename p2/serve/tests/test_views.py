"""p2 serve tests"""
import os
from shutil import rmtree
from uuid import uuid4

import requests
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from guardian.shortcuts import assign_perm, get_anonymous_user

from p2.api.models import APIKey
from p2.core.models import Blob, Storage, Volume
from p2.serve.models import ServeRule
from p2.storage.local.constants import TAG_ROOT_PATH


class ServeViewTests(LiveServerTestCase):
    """Test ServeView"""

    def setUp(self):
        super().setUp()
        self.storage_path = './storage/local-unittest-serve/'
        self.user = User.objects.create_user(
            username='p2_unittest',
            email='test@test.test',
            password=uuid4().hex)
        self.access_key, _ = APIKey.objects.get_or_create(
            user=self.user)
        self.storage = Storage.objects.create(
            name='p2_serve_unittest',
            controller_path='p2.storage.local.controller.LocalStorageController',
            tags={
                TAG_ROOT_PATH: self.storage_path
            })
        self.volume = Volume.objects.create(
            name='test-1', storage=self.storage)
        assign_perm('p2_core.use_volume', self.user, self.volume)

    def tearDown(self):
        rmtree(self.storage_path)

    def test_serve_simple(self):
        """Test Simple Serving"""
        ServeRule.objects.create(
            name='unittest-simple',
            match='.*',
            blob_query='path=/%(path)s')
        blob = Blob.objects.create(
            path='/test-aA0!-\\|/[.png',
            volume=self.volume)
        blob.write(os.urandom(2048))
        blob.save()
        assign_perm('p2_core.view_blob', get_anonymous_user(), blob)
        response = requests.get(self.live_server_url + blob.path)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, blob.read())
        self.assertEqual(response.headers['content-type'], 'application/octet-stream')

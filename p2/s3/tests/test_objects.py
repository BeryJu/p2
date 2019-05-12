"""S3 Object tests"""
from shutil import rmtree
from uuid import uuid4

import boto3
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from guardian.shortcuts import assign_perm

from p2.api.models import APIKey
from p2.core.models import Storage, Volume
from p2.s3.constants import TAG_S3_DEFAULT_STORAGE
from p2.storage.local.constants import TAG_ROOT_PATH


class ObjectTests(LiveServerTestCase):
    """Test Object-related operations"""

    def setUp(self):
        super().setUp()
        self.storage_path = './storage/local-unittest-s3/'
        self.user = User.objects.create_user(
            username='p2_unittest',
            email='test@test.test',
            password=uuid4().hex)
        self.access_key, _ = APIKey.objects.get_or_create(
            user=self.user)
        self.storage = Storage.objects.create(
            name='p2_s3_unittest',
            controller_path='p2.storage.local.controller.LocalStorageController',
            tags={
                TAG_S3_DEFAULT_STORAGE: True,
                TAG_ROOT_PATH: self.storage_path
            })
        self.volume = Volume.objects.create(
            name='test-1', storage=self.storage)
        assign_perm('p2_core.use_volume', self.user, self.volume)
        session = boto3.session.Session()
        self.boto3 = session.client(
            service_name='s3',
            aws_access_key_id=self.access_key.access_key,
            aws_secret_access_key=self.access_key.secret_key,
            endpoint_url=self.live_server_url,
        )

    def tearDown(self):
        rmtree(self.storage_path)

    def test_create_object(self):
        """Test bucket list operation"""
        data = b'this is test data'
        self.boto3.put_object(
            Body=data,
            Bucket='test-1',
            Key='test file.txt')

"""S3 Bucket tests"""
from uuid import uuid4

import boto3
from django.contrib.auth.models import User
from django.test import LiveServerTestCase
from guardian.shortcuts import assign_perm

from p2.core.models import BaseStorage, Volume
from p2.s3.models import S3AccessKey


class BucketTests(LiveServerTestCase):
    """Test Bucket-related operations"""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username='p2_unittest',
            email='test@test.test',
            password=uuid4().hex)
        self.access_key, _ = S3AccessKey.objects.get_or_create(
            user=self.user,
            defaults={
                'access_key': uuid4().hex,
                'secret_key': uuid4().hex,
            })
        self.storage = BaseStorage.objects.create(
            name='p2_s3_unittest',
            tags={
                'default.s3.p2.io': True
            })
        session = boto3.session.Session()
        self.boto3 = session.client(
            service_name='s3',
            aws_access_key_id=self.access_key.access_key,
            aws_secret_access_key=self.access_key.secret_key,
            endpoint_url=self.live_server_url+'/s3',
        )

    def test_list_buckets(self):
        """Test bucket list operation"""
        self.assertEqual(len(self.boto3.list_buckets()['Buckets']), 0)
        volume = Volume.objects.create(name='test-1', storage=self.storage)
        assign_perm('use_volume', self.user, volume)
        self.assertEqual(len(self.boto3.list_buckets()['Buckets']), 1)
        self.assertEqual(self.boto3.list_buckets()['Buckets'][0]['Name'], 'test-1')
        volume.delete()

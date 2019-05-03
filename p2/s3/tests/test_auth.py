"""S3 Auth tests"""
from uuid import uuid4
from xml.etree import ElementTree

import boto3
import requests
from botocore.exceptions import ClientError
from django.contrib.auth.models import User
from django.test import LiveServerTestCase

from p2.s3.constants import ErrorCodes
from p2.s3.models import S3AccessKey


class AuthenticationTests(LiveServerTestCase):
    """Test Authentication"""

    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username='p2_unittest',
            email='test@test.test',
            password=uuid4().hex)
        self.access_key, _ = S3AccessKey.objects.get_or_create(
            user=self.user)
        self.session = boto3.session.Session()

    def test_unknown_access_key(self):
        """Test with an unknown access key"""
        boto3 = self.session.client(
            service_name='s3',
            aws_access_key_id="invalid",
            aws_secret_access_key="invalid",
            endpoint_url=self.live_server_url)
        with self.assertRaises(ClientError):
            boto3.list_buckets()

    def test_querystring(self):
        """Test a request with a querystring"""
        boto3 = self.session.client(
            service_name='s3',
            aws_access_key_id=self.access_key.access_key,
            aws_secret_access_key=self.access_key.secret_key,
            endpoint_url=self.live_server_url)
        versions = boto3.get_bucket_versioning(Bucket='test')
        self.assertEqual(versions['Status'], 'Disabled')

    def test_without_auth(self):
        """Test request without authorization header"""
        tree = ElementTree.fromstring(requests.get(self.live_server_url, headers={
            'x-amz-date': 'test'}).content)
        for child in tree:
            # pylint: disable=unsubscriptable-object
            self.assertEqual(child.text, ErrorCodes.ACCESS_DENIED.value[0])

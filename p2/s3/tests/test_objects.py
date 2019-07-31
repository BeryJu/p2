"""S3 Object tests"""

from botocore.exceptions import ClientError

from p2.core.models import Blob
from p2.s3.tests.utils import S3TestCase


class ObjectTests(S3TestCase):
    """Test Object-related operations"""

    def test_no_such_bucket(self):
        """Test That no-such-bucket error is raised"""
        with self.assertRaises(ClientError):
            self.boto3.get_object(Bucket='non-existant-bucket', Key='test file.txt')

    def test_create_object(self):
        """Test Object creation"""
        data = b'this is test data'
        self.boto3.put_object(
            Body=data,
            Bucket='test-1',
            Key='test file.txt')
        blob = Blob.objects.get(path='/test file.txt')
        self.assertEqual(blob.read(), data)

    def test_head_object(self):
        """Test Object HEAD Operation"""
        self.boto3.put_object(
            Body=b'this is test data',
            Bucket='test-1',
            Key='test file.txt')
        response = self.boto3.head_object(
            Bucket='test-1',
            Key='test file.txt')
        self.assertEqual(response.get('ResponseMetadata').get('HTTPStatusCode'), 200)

    def test_head_object_no_key(self):
        """Test Object HEAD Operation (No Key)"""
        with self.assertRaises(ClientError):
            self.boto3.head_object(
                Bucket='test-1',
                Key='test fileaaa.txt')

    def test_get_object(self):
        """Test Object retrieval"""
        data = b'this is test data'
        self.boto3.put_object(
            Body=data,
            Bucket='test-1',
            Key='test file.txt')
        response = self.boto3.get_object(Bucket='test-1', Key='test file.txt')
        self.assertEqual(data, response['Body'].read())

    def test_get_object_no_key(self):
        """Test Object retrieval (No Key)"""
        with self.assertRaises(ClientError):
            self.boto3.get_object(
                Bucket='test-1',
                Key='test fileaaa.txt')

    def test_delete_object(self):
        """Test Object deletion"""
        self.boto3.put_object(
            Body=b'this is test data',
            Bucket='test-1',
            Key='test file.txt')
        self.boto3.delete_object(
            Bucket='test-1',
            Key='test file.txt')
        self.assertFalse(Blob.objects.filter(path='/test file.txt').exists())

"""S3 Object tests"""

from p2.s3.tests.utils import S3TestCase


class ObjectTests(S3TestCase):
    """Test Object-related operations"""

    def test_create_object(self):
        """Test bucket list operation"""
        data = b'this is test data'
        self.boto3.put_object(
            Body=data,
            Bucket='test-1',
            Key='test file.txt')

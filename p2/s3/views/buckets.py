import xml.etree.ElementTree as xml

from django.views.decorators.csrf import csrf_exempt

from p2.s3.auth import S3Authentication
from p2.s3.http import XMLResponse


class BucketView(S3Authentication):

    @csrf_exempt
    def dispatch(self, request, bucket):
        if request.method == 'GET':
            if "versioning" in request.GET:
                return self.versioning(request, bucket)
            return self.list(request, bucket)

    def versioning(self, request, bucket):
        """Versioning API Method"""
        # https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETversioningStatus.html
        root = xml.Element("{http://s3.amazonaws.com/doc/2006-03-01/}VersioningConfiguration")

        xml.SubElement(root, "Status").text = "Disabled"

        return XMLResponse(root)

    def list(self, request, bucket):
        """Bucket List API Method"""

        # https://docs.aws.amazon.com/AmazonS3/latest/API/v2-RESTBucketGET.html
        root = xml.Element("{http://s3.amazonaws.com/doc/2006-03-01}ListBucketResult")

        xml.SubElement(root, "Name").text = "test"
        xml.SubElement(root, "Prefix").text = ''
        xml.SubElement(root, "KeyCount").text = "2"
        xml.SubElement(root, "MaxKeys").text = "1000"
        xml.SubElement(root, "Delimiter").text = '/'
        xml.SubElement(root, "IsTruncated").text = 'false'

        content = xml.Element("Contents")
        xml.SubElement(content, "Key").text = "my-image.jpg"
        xml.SubElement(content, "LastModified").text = "2009-10-12T17:50:30.000Z"
        xml.SubElement(content, "ETag").text = "&quot;fba9dede5f27731c9771645a39863328&quot;"
        xml.SubElement(content, "Size").text = "434234"
        xml.SubElement(content, "StorageClass").text = "STANDARD"

        root.append(content)

        return XMLResponse(root)

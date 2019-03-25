"""p2 S3 Bucket-related Views"""
from xml.etree import ElementTree

from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from p2.core.models import Volume
from p2.s3.auth import S3Authentication
from p2.s3.constants import XML_NAMESPACE
from p2.s3.http import XMLResponse


class BucketView(S3Authentication):
    """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketOps.html"""

    @csrf_exempt
    def dispatch(self, request, bucket):
        if request.method == 'GET':
            if "versioning" in request.GET:
                return self.versioning(request, bucket)
            return self.list(request, bucket)
        return super().dispatch(self, request, bucket)

    def versioning(self, request, bucket):
        """Versioning API Method"""
        # https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETversioningStatus.html
        root = ElementTree.Element("{%s}VersioningConfiguration" % XML_NAMESPACE)

        ElementTree.SubElement(root, "Status").text = "Disabled"

        return XMLResponse(root)

    def list(self, request, bucket):
        """Bucket List API Method"""
        # https://docs.aws.amazon.com/AmazonS3/latest/API/v2-RESTBucketGET.html
        root = ElementTree.Element("{%s}ListBucketResult" % XML_NAMESPACE)
        volume = get_object_or_404(Volume, name=bucket)
        # blobs = Blob.objects.filter(volume=volume)

        ElementTree.SubElement(root, "Name").text = volume.name
        ElementTree.SubElement(root, "Prefix").text = ''
        ElementTree.SubElement(root, "KeyCount").text = "2"
        ElementTree.SubElement(root, "MaxKeys").text = "1000"
        ElementTree.SubElement(root, "Delimiter").text = '/'
        ElementTree.SubElement(root, "IsTruncated").text = 'false'

        content = ElementTree.Element("Contents")
        ElementTree.SubElement(content, "Key").text = "my-image.jpg"
        ElementTree.SubElement(content, "LastModified").text = "2009-10-12T17:50:30.000Z"
        ElementTree.SubElement(content, "ETag").text = "&quot;fba9ede5f27731c9771645a39863328&quot;"
        ElementTree.SubElement(content, "Size").text = "434234"
        ElementTree.SubElement(content, "StorageClass").text = "STANDARD"

        root.append(content)

        return XMLResponse(root)

"""p2 S3 Bucket-related Views"""
from xml.etree import ElementTree

from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from guardian.shortcuts import get_objects_for_user

from p2.core.models import Blob, Volume
from p2.s3.auth import S3Authentication
from p2.s3.constants import XML_NAMESPACE
from p2.s3.http import XMLResponse


class BucketView(S3Authentication):
    """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketOps.html"""

    def versioning(self, request, bucket):
        """Versioning API Method"""
        # https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETversioningStatus.html
        root = ElementTree.Element("{%s}VersioningConfiguration" % XML_NAMESPACE)

        ElementTree.SubElement(root, "Status").text = "Disabled"

        return XMLResponse(root)

    def get(self, request, bucket):
        """Bucket List API Method"""
        if "versioning" in request.GET:
            return self.versioning(request, bucket)
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

        for blob in get_objects_for_user(self.request.user, 'view_blob', Blob):
            content = ElementTree.Element("Contents")
            ElementTree.SubElement(content, "Key").text = blob.path[1:]
            ElementTree.SubElement(
                content, "LastModified").text = blob.attributes.get('date_updated')
            # ElementTree.SubElement(
            #     content, "ETag").text = "&quot;fba9ede5f27731c9771645a39863328&quot;"
            ElementTree.SubElement(content, "Size").text = str(
                blob.attributes.get('size:bytes', 0))
            ElementTree.SubElement(content, "StorageClass").text = blob.storage_instance.provider
            root.append(content)

        return XMLResponse(root)

    def put(self, request, bucket):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUTlifecycle.html"""
        # TODO: Implement bucket creation via API
        # if 'lifecycle' in request.GET:
        return HttpResponse(status=200)

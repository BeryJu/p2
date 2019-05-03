"""p2 S3 Bucket-related Views"""
from xml.etree import ElementTree

from django.http import HttpResponse
from guardian.shortcuts import get_objects_for_user

from p2.core.constants import (ATTR_BLOB_HASH_SHA512, ATTR_BLOB_SIZE_BYTES,
                               ATTR_BLOB_STAT_MTIME)
from p2.core.models import Volume
from p2.lib.shortcuts import get_object_for_user_or_404
from p2.s3.auth import S3Authentication
from p2.s3.constants import (TAG_S3_DEFAULT_STORAGE, TAG_S3_STORAGE_CLASS,
                             XML_NAMESPACE)
from p2.s3.http import XMLResponse


class BucketView(S3Authentication):
    """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketOps.html"""

    def get(self, request, *args, **kwargs):
        """Boilerplate to pass request to correct handler"""
        if "versioning" in request.GET:
            return self.handler_versioning(request, *args, **kwargs)
        return self.handler_list(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        """Boilerplate to pass request to correct handler"""
        return self.handler_create(request, *args, **kwargs)

    def handler_versioning(self, request, bucket):
        """Versioning API Method"""
        # https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETversioningStatus.html
        root = ElementTree.Element("{%s}VersioningConfiguration" % XML_NAMESPACE)

        ElementTree.SubElement(root, "Status").text = "Disabled"

        return XMLResponse(root)

    def handler_list(self, request, bucket):
        """Bucket List API Method"""
        # https://docs.aws.amazon.com/AmazonS3/latest/API/v2-RESTBucketGET.html
        root = ElementTree.Element("{%s}ListBucketResult" % XML_NAMESPACE)
        volume = get_object_for_user_or_404(self.request.user, 'p2_core.use_volume', name=bucket)
        blobs = get_objects_for_user(self.request.user, 'p2_core.view_blob')

        ElementTree.SubElement(root, "Name").text = volume.name
        ElementTree.SubElement(root, "Prefix").text = ''
        ElementTree.SubElement(root, "KeyCount").text = str(len(blobs))
        ElementTree.SubElement(root, "MaxKeys").text = "1000"
        ElementTree.SubElement(root, "Delimiter").text = '/'
        ElementTree.SubElement(root, "IsTruncated").text = 'false'

        for blob in blobs:
            content = ElementTree.Element("Contents")
            ElementTree.SubElement(content, "Key").text = blob.path[1:]
            ElementTree.SubElement(
                content, "LastModified").text = blob.attributes.get(ATTR_BLOB_STAT_MTIME)
            ElementTree.SubElement(
                content, "ETag").text = blob.attributes.get(ATTR_BLOB_HASH_SHA512)
            ElementTree.SubElement(content, "Size").text = str(
                blob.attributes.get(ATTR_BLOB_SIZE_BYTES, 0))
            ElementTree.SubElement(content, "StorageClass").text = \
                blob.volume.storage.controller.tags.get(TAG_S3_STORAGE_CLASS, 'default')
            root.append(content)

        return XMLResponse(root)

    def handler_create(self, request, bucket):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUT.html"""
        default_storage = get_object_for_user_or_404(request.user, 'p2_core.use_storage', **{
            'tags_%s' % TAG_S3_DEFAULT_STORAGE: True
        })
        bucket, _ = Volume.objects.get_or_create(name=bucket, defaults={
            'storage': default_storage
        })
        return HttpResponse(status=200)

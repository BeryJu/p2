"""p2 S3 Bucket-related Views"""
from xml.etree import ElementTree

from django.http import HttpResponse
from guardian.shortcuts import get_objects_for_user

from p2.core.constants import (ATTR_BLOB_HASH_MD5, ATTR_BLOB_SIZE_BYTES,
                               ATTR_BLOB_STAT_MTIME)
from p2.core.models import Volume
from p2.lib.shortcuts import get_object_for_user_or_404
from p2.s3.auth import S3Authentication
from p2.s3.constants import (TAG_S3_DEFAULT_STORAGE, TAG_S3_STORAGE_CLASS,
                             XML_NAMESPACE)
from p2.s3.http import XMLResponse
from p2.ui.views.core.blob import FileBrowserView


class BucketView(S3Authentication):
    """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketOps.html"""

    def get(self, request, *args, **kwargs):
        """Boilerplate to pass request to correct handler"""
        if "versioning" in request.GET:
            return self.handler_versioning(request, *args, **kwargs)
        if 'uploads' in request.GET:
            return self.handler_uploads(request, *args, **kwargs)
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

    def handler_uploads(self, request, bucket):
        """Versioning API Method"""
        # https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketGETversioningStatus.html
        root = ElementTree.Element("{%s}VersioningConfiguration" % XML_NAMESPACE)

        ElementTree.SubElement(root, "Status").text = "Disabled"

        return XMLResponse(root)

    def handler_list(self, request, bucket):
        """Bucket List API Method"""
        # https://docs.aws.amazon.com/AmazonS3/latest/API/v2-RESTBucketGET.html
        root = ElementTree.Element("{%s}ListBucketResult" % XML_NAMESPACE)
        volume = get_object_for_user_or_404(
            self.request.user, 'p2_core.list_volume_contents', name=bucket)
        prefix = '/' + request.GET.get('prefix', '')[:-1]
        blobs = get_objects_for_user(self.request.user, 'p2_core.view_blob').filter(
            prefix=prefix
        )

        ElementTree.SubElement(root, "Name").text = volume.name
        ElementTree.SubElement(root, "Prefix").text = prefix
        ElementTree.SubElement(root, "KeyCount").text = str(len(blobs))
        ElementTree.SubElement(root, "MaxKeys").text = "1000"
        ElementTree.SubElement(root, "Delimiter").text = '/'
        ElementTree.SubElement(root, "IsTruncated").text = 'false'

        # append all blobs
        for blob in blobs:
            content = ElementTree.Element("Contents")
            ElementTree.SubElement(content, "Key").text = blob.path[1:]
            ElementTree.SubElement(
                content, "LastModified").text = blob.attributes.get(ATTR_BLOB_STAT_MTIME)
            ElementTree.SubElement(
                content, "ETag").text = blob.attributes.get(ATTR_BLOB_HASH_MD5)
            ElementTree.SubElement(content, "Size").text = str(
                blob.attributes.get(ATTR_BLOB_SIZE_BYTES, 0))
            ElementTree.SubElement(content, "StorageClass").text = \
                blob.volume.storage.controller.tags.get(TAG_S3_STORAGE_CLASS, 'default')
            root.append(content)

        # append CommonPrefixes
        common_prefixes = ElementTree.Element("CommonPrefixes")
        # TODO: move this logic to a class in p2.lib
        fbv = FileBrowserView()
        fbv.request = request
        for prefix in fbv.build_prefix_list(prefix, volume, add_up_prefix=False):
            ElementTree.SubElement(
                common_prefixes, 'Prefix').text = prefix.get('relative_prefix')

        root.append(common_prefixes)

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

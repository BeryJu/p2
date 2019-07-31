"""p2 S3 Bucket-related Views"""
from xml.etree import ElementTree

from django.core.paginator import Paginator
from django.http import HttpResponse
from guardian.shortcuts import assign_perm, get_objects_for_user

from p2.core.constants import (ATTR_BLOB_HASH_MD5, ATTR_BLOB_SIZE_BYTES,
                               ATTR_BLOB_STAT_MTIME)
from p2.core.models import Volume
from p2.core.prefix_helper import PrefixHelper, make_absolute_prefix
from p2.s3.constants import (TAG_S3_DEFAULT_STORAGE, TAG_S3_STORAGE_CLASS,
                             XML_NAMESPACE)
from p2.s3.errors import AWSAccessDenied
from p2.s3.http import XMLResponse
from p2.s3.views.common import S3View


class BucketView(S3View):
    """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketOps.html"""

    def get(self, request, *args, **kwargs):
        """Boilerplate to pass request to correct handler"""
        if "versioning" in request.GET:
            return self.handler_versioning(request, *args, **kwargs)
        if 'uploads' in request.GET:
            return self.handler_uploads(request, *args, **kwargs)
        return self.handler_list(request, *args, **kwargs)

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

    # pylint: disable=too-many-locals
    def handler_list(self, request, bucket):
        """Bucket List API Method"""
        # https://docs.aws.amazon.com/AmazonS3/latest/API/v2-RESTBucketGET.html
        root = ElementTree.Element("{%s}ListBucketResult" % XML_NAMESPACE)
        volume = self.get_volume('p2_core.list_volume_contents', name=bucket)
        requested_prefix = request.GET.get('prefix', '')
        blobs = get_objects_for_user(self.request.user, 'p2_core.view_blob').filter(
            prefix=make_absolute_prefix(requested_prefix),
            volume=volume,
        ).order_by('path')

        max_keys = int(self.request.GET.get('max-keys', 100))
        encoding_type = self.request.GET.get('encoding-type', 'url')
        delimiter = self.request.GET.get('delimiter', '/')
        paginator = Paginator(blobs, max_keys)
        is_truncated = max_keys < paginator.count

        ElementTree.SubElement(root, "Name").text = volume.name
        ElementTree.SubElement(root, "Prefix").text = requested_prefix
        ElementTree.SubElement(root, "KeyCount").text = str(len(paginator.page(1).object_list))
        ElementTree.SubElement(root, "MaxKeys").text = str(max_keys)
        ElementTree.SubElement(root, "Delimiter").text = delimiter
        ElementTree.SubElement(root, "EncodingType").text = encoding_type
        ElementTree.SubElement(root, "IsTruncated").text = str(is_truncated).lower()

        # append all blobs
        for blob in paginator.page(1):
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
        helper = PrefixHelper(request.user, volume, make_absolute_prefix(requested_prefix))
        # Disable intermediate prefixes since that's handled by the client
        helper.collect(max_levels=-1)

        for virtual_prefix in helper.prefixes:
            ElementTree.SubElement(
                common_prefixes, 'Prefix').text = virtual_prefix.absolute_path[1:] + "/"

        if common_prefixes:
            root.append(common_prefixes)

        return XMLResponse(root)

    def put(self, request, bucket):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketPUT.html"""
        storages = get_objects_for_user(request.user, 'p2_core.use_storage').filter(**{
            'tags__%s' % TAG_S3_DEFAULT_STORAGE: True
        })
        if not storages.exists():
            raise AWSAccessDenied
        if not request.user.has_perm('p2_core.add_volume'):
            raise AWSAccessDenied
        bucket, _ = Volume.objects.get_or_create(name=bucket, defaults={
            'storage': storages.first()
        })
        for permission in ['view_volume', 'change_volume', 'delete_volume',
                           'use_volume', 'list_volume_contents']:
            assign_perm('p2_core.%s' % permission, request.user, bucket)
        return HttpResponse(status=200)

    def delete(self, request, bucket):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTBucketDELETE.html"""
        volume = self.get_volume('p2_core.delete_volume', name=bucket)
        volume.delete()
        return HttpResponse(status=204)

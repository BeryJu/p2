"""common s3 views"""
import base64
from hashlib import md5
from logging import getLogger

from django.views import View
from django.views.decorators.csrf import csrf_exempt
from guardian.shortcuts import get_objects_for_user

from p2.core.models import Blob, Volume
from p2.s3.errors import (AWSBadDigest, AWSError, AWSInvalidDigest,
                          AWSNoSuchBucket, AWSNoSuchKey)

CONTENT_MD5_HEADER = 'HTTP_CONTENT_MD5'
X_AMZ_ACL_HEADER = 'HTTP_X_AMZ_ACL'
LOGGER = getLogger(__name__)

VALID_ACLS = ["private",
              "public-read",
              "public-read-write",
              "aws-exec-read",
              "authenticated-read",
              "bucket-owner-read",
              "bucket-owner-full-control"]

class S3View(View):
    """Base View for all S3 Views. Checks for common Headers and does database lookups."""

    def _check_content_md5(self):
        """Validate Content-MD5 Header (length and validity)"""
        if CONTENT_MD5_HEADER in self.request.META:
            if self.request.META.get(CONTENT_MD5_HEADER) == '':
                raise AWSInvalidDigest
            if len(self.request.META.get(CONTENT_MD5_HEADER)) < 24:
                raise AWSInvalidDigest
            hasher = md5()
            hasher.update(self.request.body)
            ours = base64.b64encode(hasher.digest()).decode('utf-8')
            if self.request.META.get(CONTENT_MD5_HEADER) != ours:
                LOGGER.debug(self.request.body)
                LOGGER.debug("Got bad digest: theirs %s vs ours %s",
                             self.request.META.get(CONTENT_MD5_HEADER), ours)
                raise AWSBadDigest

    def apply_acl_permissions(self):
        """Parse x-amz-acl Header into p2 permissions, returned as List"""
        header = self.request.META.get(X_AMZ_ACL_HEADER)
        if not header:
            return
        if header not in VALID_ACLS:
            raise AWSError

    def get_volume(self, perm, **lookup) -> Volume:
        """Small wrapper to get volume and raise AWS Error if not found"""
        volumes = get_objects_for_user(self.request.user, perm, Volume).filter(**lookup)
        if not volumes.exists():
            raise AWSNoSuchBucket
        return volumes.first()

    def get_blob(self, perm, **lookup) -> Blob:
        """Small wrapper to get blob and raise AWS Error if not found"""
        blobs = get_objects_for_user(self.request.user, perm, Blob).filter(**lookup)
        if not blobs.exists():
            raise AWSNoSuchKey
        return blobs.first()

    @csrf_exempt
    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)
        self._check_content_md5()
        self.apply_acl_permissions()

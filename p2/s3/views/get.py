"""p2 S3 views"""
from xml.etree import ElementTree

from django.views import View
from guardian.shortcuts import get_objects_for_user

from p2.s3.constants import XML_NAMESPACE
from p2.s3.http import XMLResponse


class ListView(View):
    """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTServiceGET.html"""

    def get(self, request):
        """Return list of Buckets"""
        root = ElementTree.Element("{%s}ListAllMyBucketsResult" % XML_NAMESPACE)
        owner = ElementTree.Element("Owner")

        ElementTree.SubElement(owner, 'ID').text = str(request.user.id)
        ElementTree.SubElement(owner, 'DisplayName').text = request.user.username

        buckets = ElementTree.Element('Buckets')

        for volume in get_objects_for_user(self.request.user, 'p2_core.use_volume'):
            bucket = ElementTree.Element("Bucket")
            ElementTree.SubElement(bucket, "Name").text = volume.name
            ElementTree.SubElement(bucket, "CreationDate").text = "2006-02-03T16:45:09.000Z"
            buckets.append(bucket)

        root.append(owner)
        root.append(buckets)

        return XMLResponse(root)

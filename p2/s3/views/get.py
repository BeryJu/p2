"""p2 S3 views"""
from xml.etree import ElementTree

from guardian.shortcuts import get_objects_for_user

from p2.s3.auth import S3Authentication
from p2.s3.http import XMLResponse


class ListView(S3Authentication):
    """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTServiceGET.html"""

    def get(self, request):
        """Return list of Buckets"""
        root = ElementTree.Element("{http://s3.amazonaws.com/doc/2006-03-01}ListAllMyBucketsResult")
        owner = ElementTree.Element("Owner")

        owner_id = ElementTree.SubElement(owner, 'ID')
        owner_id.text = str(request.user.id)
        owner_display_name = ElementTree.SubElement(owner, 'DisplayName')
        owner_display_name.text = request.user.username

        buckets = ElementTree.Element('Buckets')

        for volume in get_objects_for_user(self.request.user, 'p2_core.use_volume'):
            bucket = ElementTree.Element("Bucket")
            bucket_name = ElementTree.SubElement(bucket, "Name")
            bucket_name.text = volume.name
            bucket_creation_date = ElementTree.SubElement(bucket, "CreationDate")
            bucket_creation_date.text = "2006-02-03T16:45:09.000Z"
            buckets.append(bucket)

        root.append(owner)
        root.append(buckets)

        return XMLResponse(root)

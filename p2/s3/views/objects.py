"""p2 S3 Object views"""
# from xml.etree import ElementTree

from django.http.response import HttpResponse

from p2.s3.auth import S3Authentication


class ObjectView(S3Authentication):
    """Object related views"""

    def get(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectGET.html"""
        return HttpResponse(status=200)

    def put(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectPUT.html"""
        return HttpResponse(status=200)

    def delete(self, request, bucket, path):
        """https://docs.aws.amazon.com/AmazonS3/latest/API/RESTObjectDELETE.html"""
        return HttpResponse(status=204)

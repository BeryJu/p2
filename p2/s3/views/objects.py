import xml.etree.ElementTree as xml

from django.http.response import FileResponse, HttpResponse

from p2.s3.auth import S3Authentication
from p2.s3.http import XMLResponse


class ObjectView(S3Authentication):

    def get(self, request, bucket, path):
        # return FileResponse()
        return HttpResponse(status=200)

    def put(self, request, bucket, path):
        return HttpResponse(status=200)

    def delete(self, request, bucket, path):
        return HttpResponse(status=204)

"""AWS API Constants"""
from enum import Enum


class ErrorCodes(Enum):
    """Error codes from https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html"""

    ACCESS_DENIED = "AccessDenied", 401
    NOT_IMPLEMENTED = "NotImplemented", 501
    NO_SUCH_KEY = "NoSuchKey", 404
    NO_SUCH_BUCKET = "NoSuchBucket", 404
    SIGNATURE_DOES_NOT_MATCH = "SignatureDoesNotMatch", 403

XML_NAMESPACE = "http://s3.amazonaws.com/doc/2006-03-01/"

TAG_S3_STORAGE_CLASS = 's3.p2.io/storage_class'
TAG_S3_DEFAULT_STORAGE = 's3.p2.io/default_storage'

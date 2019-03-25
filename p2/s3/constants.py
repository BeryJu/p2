"""AWS API Constants"""
from enum import Enum


class ErrorCodes(Enum):
    """Error codes from https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html"""

    ACCESS_DENIED = "AccessDenied", 401
    NOT_IMPLEMENTED = "NotImplemented", 501

XML_NAMESPACE = "http://s3.amazonaws.com/doc/2006-03-01/"

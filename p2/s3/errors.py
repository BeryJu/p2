"""AWS API Errors"""

class AWSError(Exception):
    """Base-class for all AWS Errors"""

    code = ''
    status = 400


class AWSSignatureMismatch(AWSError):
    """Error codes from https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html"""

    code = 'SignatureDoesNotMatch'
    status = 403


class AWSAccessDenied(AWSError):
    """Error codes from https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html"""

    code = 'AccessDenied'
    status = 401


class AWSNotImplemented(AWSError):
    """Error codes from https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html"""

    code = 'NotImplemented'
    status = 501


class AWSNoSuchKey(AWSError):
    """Error codes from https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html"""

    code = 'NoSuchKey'
    status = 404


class AWSNoSuchBucket(AWSError):
    """Error codes from https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html"""

    code = 'NoSuchBucket'
    status = 404


class AWSInvalidHMAC(AWSError):
    """Error codes from https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html"""

    code = 'InvalidRequest'
    status = 400


class AWSContentSignatureMismatch(AWSError):
    """Error codes from https://docs.aws.amazon.com/AmazonS3/latest/API/ErrorResponses.html"""

    code = 'XAmzContentSHA256Mismatch'
    status = 403

"""p2 quota exceptions"""

from p2.core.exceptions import BlobException


class QuotaExceededException(BlobException):
    """Exception raised when ACTION_BLOCK is selected."""

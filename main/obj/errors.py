
class InvalidFileTypeError(Exception):
    """
    Raised when the upload file type doesn't match the
    desired type.
    """
    pass


class OutboundNetworkError(Exception):
    """
    Raised when undesired result is proposed when
    expecting a response from an outbound source.
    """
    pass

class ResponseLengthMismatchError(Exception):
    """
    Raised when the response length does not match
    the input length when it's expected that the 
    response should match to the input one-by-one.
    """
    pass
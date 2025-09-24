class CoinglassRequestError(Exception):
    """ Generic exception for API requests """

    def __init__(self, code: int, msg: str):
        self.code = code
        self.msg = msg

    def __str__(self):
        return f"(code={self.code}) {self.msg}"


class RateLimitExceededError(CoinglassRequestError):
    """ Raised when API rate limit is exceeded """

    def __init__(self, msg: str):
        super().__init__(code=10004, msg=msg)


class NoDataReturnedError(Exception):
    """ Raised when no data is returned from API """

    def __init__(self):
        super().__init__("API request returned no data")


class CoinglassParameterWarning(Warning):
    """ Warning for (potentially) invalid parameters """
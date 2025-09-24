import unittest
from coinglass_api.exceptions import CoinglassRequestError, RateLimitExceededError, NoDataReturnedError


class TestExceptions(unittest.TestCase):

    def test_coinglass_request_error(self):
        error = CoinglassRequestError(code=10001, msg="Invalid request")
        self.assertEqual(error.code, 10001)
        self.assertEqual(error.msg, "Invalid request")
        self.assertEqual(str(error), "(code=10001) Invalid request")

    def test_rate_limit_exceeded_error(self):
        error = RateLimitExceededError("Rate limit exceeded for this endpoint")
        self.assertEqual(error.code, 10004)
        self.assertEqual(error.msg, "Rate limit exceeded for this endpoint")
        self.assertEqual(str(error), "(code=10004) Rate limit exceeded for this endpoint")

    def test_no_data_returned_error(self):
        error = NoDataReturnedError()
        self.assertEqual(str(error), "API request returned no data")


if __name__ == '__main__':
    unittest.main()
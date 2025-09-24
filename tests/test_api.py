import unittest
from unittest.mock import patch, MagicMock
import pandas as pd
from coinglass_api.api import CoinglassAPI
from coinglass_api.exceptions import CoinglassRequestError, NoDataReturnedError, RateLimitExceededError


class TestCoinglassAPI(unittest.TestCase):
    def setUp(self):
        self.api = CoinglassAPI(api_key="test_key")

    @patch('requests.Session.request')
    def test_futures_markets_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": [{"symbol": "BTC", "price": 50000}]}
        mock_request.return_value = mock_response

        df = self.api.futures_markets(symbol="BTC")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("symbol", df.columns)

    @patch('requests.Session.request')
    def test_funding_rate_history_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": [{"r": 0.01, "t": 1622548800000}]}
        mock_request.return_value = mock_response

        df = self.api.funding_rate_history(symbol="BTC", interval="h8")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("r", df.columns)
        self.assertEqual(df.index.name, "time")

    @patch('requests.Session.request')
    def test_open_interest_history_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": [{"oi": 1000, "t": 1622548800000}]}
        mock_request.return_value = mock_response

        df = self.api.open_interest_history(symbol="BTC", interval="h8")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("oi", df.columns)
        self.assertEqual(df.index.name, "time")

    @patch('requests.Session.request')
    def test_liquidation_history_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": [{"v": 1000, "t": 1622548800000}]}
        mock_request.return_value = mock_response

        df = self.api.liquidation_history(symbol="BTC", interval="h8")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("v", df.columns)
        self.assertEqual(df.index.name, "time")

    @patch('requests.Session.request')
    def test_long_short_ratio_history_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": [{"lsr": 1.5, "t": 1622548800000}]}
        mock_request.return_value = mock_response

        df = self.api.long_short_ratio_history(symbol="BTC", interval="h8")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("lsr", df.columns)
        self.assertEqual(df.index.name, "time")

    @patch('requests.Session.request')
    def test_options_info_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": [{"oi": 1000, "vol": 500}]}
        mock_request.return_value = mock_response

        df = self.api.options_info(symbol="BTC")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("oi", df.columns)

    @patch('requests.Session.request')
    def test_options_exchange_oi_history_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": [{"oi": 1000, "createTime": 1622548800000}]}
        mock_request.return_value = mock_response

        df = self.api.options_exchange_oi_history(symbol="BTC", exchange="Deribit")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("oi", df.columns)
        self.assertEqual(df.index.name, "time")

    @patch('requests.Session.request')
    def test_exchange_balance_history_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": [{"balance": 1000, "createTime": 1622548800000}]}
        mock_request.return_value = mock_response

        df = self.api.exchange_balance_history(exchange="Binance", asset="BTC")
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("balance", df.columns)
        self.assertEqual(df.index.name, "time")

    @patch('requests.Session.request')
    def test_fear_and_greed_index_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": [{"value": 50, "t": 1622548800000}]}
        mock_request.return_value = mock_response

        df = self.api.fear_and_greed_index()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("value", df.columns)
        self.assertEqual(df.index.name, "time")

    @patch('requests.Session.request')
    def test_bitcoin_rainbow_chart_success(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": [{"value": 50000, "t": 1622548800000}]}
        mock_request.return_value = mock_response

        df = self.api.bitcoin_rainbow_chart()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertFalse(df.empty)
        self.assertIn("value", df.columns)
        self.assertEqual(df.index.name, "time")

    @patch('requests.Session.request')
    def test_no_data_returned(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True, "data": []}
        mock_request.return_value = mock_response

        with self.assertRaises(NoDataReturnedError):
            self.api.futures_markets(symbol="BTC")

    @patch('requests.Session.request')
    def test_rate_limit_exceeded(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": False, "code": "10004", "msg": "Rate limit exceeded"}
        mock_request.return_value = mock_response

        with self.assertRaises(RateLimitExceededError):
            self.api.futures_markets(symbol="BTC")

    @patch('requests.Session.request')
    def test_coinglass_request_error(self, mock_request):
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": False, "code": "10001", "msg": "Invalid API key"}
        mock_request.return_value = mock_response

        with self.assertRaises(CoinglassRequestError):
            self.api.futures_markets(symbol="BTC")

    def test_invalid_parameter_type(self):
        with self.assertRaises(TypeError):
            self.api.futures_markets(symbol={"wrong": "type"})


if __name__ == '__main__':
    unittest.main()
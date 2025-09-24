from typing import Optional

import pandas as pd
import requests

from .exceptions import (
    CoinglassRequestError,
    NoDataReturnedError,
    RateLimitExceededError,
)


class CoinglassAPI:
    """ Unofficial Python client for Coinglass API """

    def __init__(self, api_key: str):
        """
        Args:
            api_key: key from Coinglass, get one at
            https://www.coinglass.com/pricing
        """
        self.__api_key = api_key
        self._base_url = "https://open-api-v4.coinglass.com/api/v4/"
        self._session = requests.Session()

    def _validate_params(self, params: dict):
        # Basic validation, can be expanded
        for key, value in params.items():
            if value is not None and not isinstance(value, (str, int, float)):
                raise TypeError(f"Invalid type for parameter {key}: {type(value)}")

    def _get(self, endpoint: str, params: dict | None = None) -> dict:
        if params:
            self._validate_params(params)
            params = {k: v for k, v in params.items() if v is not None}

        headers = {
            "accept": "application/json",
            "cg-api-key": self.__api_key
        }
        url = self._base_url + endpoint
        response = self._session.request(
            method='GET',
            url=url,
            params=params,
            headers=headers,
            timeout=30
        )
        return response.json()

    @staticmethod
    def _create_dataframe(
            data: list[dict],
            time_col: str | None = None,
            unit: str | None = "ms",
            cast_objects_to_numeric: bool = False
    ) -> pd.DataFrame:
        if not data:
            return pd.DataFrame()

        df = pd.DataFrame(data)

        if time_col and time_col in df.columns:
            if time_col == "time":
                df.rename(columns={"time": "t"}, inplace=True)
                time_col = "t"

            df["time"] = pd.to_datetime(df[time_col], unit=unit)
            df.drop(columns=[time_col], inplace=True)
            df.set_index("time", inplace=True, drop=True)

            if "t" in df.columns:
                df.drop(columns=["t"], inplace=True)

        if cast_objects_to_numeric:
            for col in df.columns:
                if df[col].dtype == 'object':
                    df[col] = pd.to_numeric(df[col], errors='ignore')
        return df

    @staticmethod
    def _check_for_errors(response: dict) -> None:
        """ Check for errors in response """
        if not response.get("success", True):
            code, msg = response.get("code", "0"), response.get("msg", "Unknown error")
            if code == "10004":  # Rate limit exceeded
                raise RateLimitExceededError(msg)
            raise CoinglassRequestError(code=code, msg=msg)

        if "data" not in response or not response["data"]:
            raise NoDataReturnedError()

    def futures_markets(self, symbol: str) -> pd.DataFrame:
        response = self._get(
            endpoint="futures/coins-markets",
            params={"symbol": symbol}
        )
        self._check_for_errors(response)
        return self._create_dataframe(response["data"])

    def funding_rate_history(self, symbol: str, interval: str, limit: int = 200) -> pd.DataFrame:
        response = self._get(
            endpoint="futures/fr-ohlc-history",
            params={"symbol": symbol, "interval": interval, "limit": limit}
        )
        self._check_for_errors(response)
        return self._create_dataframe(response["data"], time_col="t")

    def open_interest_history(self, symbol: str, interval: str, limit: int = 200) -> pd.DataFrame:
        response = self._get(
            endpoint="futures/oi-ohlc-history",
            params={"symbol": symbol, "interval": interval, "limit": limit}
        )
        self._check_for_errors(response)
        return self._create_dataframe(response["data"], time_col="t")

    def liquidation_history(self, symbol: str, interval: str, limit: int = 200) -> pd.DataFrame:
        response = self._get(
            endpoint="futures/aggregated-liquidation-history",
            params={"symbol": symbol, "interval": interval, "limit": limit}
        )
        self._check_for_errors(response)
        return self._create_dataframe(response["data"], time_col="t")

    def long_short_ratio_history(self, symbol: str, interval: str, limit: int = 200) -> pd.DataFrame:
        response = self._get(
            endpoint="futures/global-longshort-account-ratio",
            params={"symbol": symbol, "interval": interval, "limit": limit}
        )
        self._check_for_errors(response)
        return self._create_dataframe(response["data"], time_col="t")

    def options_info(self, symbol: str) -> pd.DataFrame:
        response = self._get(
            endpoint="options/info",
            params={"symbol": symbol}
        )
        self._check_for_errors(response)
        return self._create_dataframe(response["data"])

    def options_exchange_oi_history(self, symbol: str, exchange: str, limit: int = 200) -> pd.DataFrame:
        response = self._get(
            endpoint="options/exchange-open-interest-history",
            params={"symbol": symbol, "exchangeName": exchange, "limit": limit}
        )
        self._check_for_errors(response)
        return self._create_dataframe(response["data"], time_col="createTime")

    def exchange_balance_history(self, exchange: str, asset: str) -> pd.DataFrame:
        response = self._get(
            endpoint="on-chain/exchange-balance-chart",
            params={"exchangeName": exchange, "assetName": asset}
        )
        self._check_for_errors(response)
        return self._create_dataframe(response["data"], time_col="createTime")

    def fear_and_greed_index(self) -> pd.DataFrame:
        response = self._get(
            endpoint="indic/crypto-fear-greed-index"
        )
        self._check_for_errors(response)
        df = self._create_dataframe(response["data"], time_col="t")
        return df

    def bitcoin_rainbow_chart(self) -> pd.DataFrame:
        response = self._get(
            endpoint="indic/bitcoin-rainbow-chart"
        )
        self._check_for_errors(response)
        df = self._create_dataframe(response["data"], time_col="t")
        return df
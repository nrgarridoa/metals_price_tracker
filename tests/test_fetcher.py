"""Tests para src/fetcher.py"""

import pandas as pd
import pytest
from unittest.mock import patch
from src.fetcher import fetch_current_price, fetch_historical, _normalize_columns


class TestNormalizeColumns:
    def test_renames_uppercase_columns(self):
        df = pd.DataFrame({"Open": [1], "Close": [2], "Volume": [3]})
        result = _normalize_columns(df)
        assert "open" in result.columns
        assert "close" in result.columns
        assert "volume" in result.columns

    def test_strips_timezone(self):
        idx = pd.to_datetime(["2025-01-01"]).tz_localize("UTC")
        df = pd.DataFrame({"Close": [100]}, index=idx)
        result = _normalize_columns(df)
        assert result.index.tz is None

    def test_handles_multiindex_columns(self):
        arrays = [["Open", "Close"], ["GC=F", "GC=F"]]
        tuples = list(zip(*arrays))
        index = pd.MultiIndex.from_tuples(tuples)
        df = pd.DataFrame([[100, 200]], columns=index)
        result = _normalize_columns(df)
        assert not isinstance(result.columns, pd.MultiIndex)


class TestFetchCurrentPrice:
    @patch("src.fetcher.yf.download")
    def test_returns_dict_on_success(self, mock_dl):
        idx = pd.to_datetime(["2025-01-01"])
        mock_dl.return_value = pd.DataFrame(
            {"Open": [100], "High": [110], "Low": [90],
             "Close": [105], "Volume": [1000]},
            index=idx,
        )
        result = fetch_current_price("GC=F")
        assert result is not None
        assert result["close"] == 105.0
        assert result["high"] == 110.0

    @patch("src.fetcher.yf.download")
    def test_returns_none_on_empty(self, mock_dl):
        mock_dl.return_value = pd.DataFrame()
        assert fetch_current_price("INVALID") is None

    @patch("src.fetcher.yf.download")
    def test_returns_none_on_exception(self, mock_dl):
        mock_dl.side_effect = Exception("Network error")
        assert fetch_current_price("GC=F") is None


class TestFetchHistorical:
    @patch("src.fetcher.yf.download")
    def test_returns_dataframe(self, mock_dl):
        idx = pd.to_datetime(["2025-01-01", "2025-01-02"])
        mock_dl.return_value = pd.DataFrame(
            {"Open": [100, 101], "Close": [105, 106],
             "Volume": [1000, 1100], "High": [110, 111],
             "Low": [90, 91]},
            index=idx,
        )
        result = fetch_historical("GC=F")
        assert not result.empty
        assert "close" in result.columns
        assert len(result) == 2

    @patch("src.fetcher.yf.download")
    def test_returns_empty_on_failure(self, mock_dl):
        mock_dl.return_value = pd.DataFrame()
        result = fetch_historical("INVALID")
        assert result.empty

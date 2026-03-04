"""Tests para src/database.py"""

import pytest
from src.database import init_db, insert_price, get_latest_price, get_history


@pytest.fixture(autouse=True)
def temp_db(tmp_path, monkeypatch):
    """Usa una BD temporal para cada test."""
    test_db = str(tmp_path / "test_metals.db")
    monkeypatch.setattr("src.database.DB_PATH", test_db)
    init_db()
    yield test_db


class TestInsertAndRetrieve:
    def test_insert_and_get_latest(self):
        insert_price("Oro", "GC=F", {
            "open": 2000, "high": 2050, "low": 1980,
            "close": 2040, "volume": 5000,
            "timestamp": "2025-01-15T10:00:00",
        })
        result = get_latest_price("GC=F")
        assert result is not None
        assert result["close"] == 2040
        assert result["metal"] == "Oro"
        assert result["ticker"] == "GC=F"

    def test_no_duplicates(self):
        data = {
            "open": 100, "high": 110, "low": 90,
            "close": 105, "volume": 500,
            "timestamp": "2025-01-15T10:00:00",
        }
        insert_price("Oro", "GC=F", data)
        insert_price("Oro", "GC=F", data)  # mismo timestamp
        history = get_history("GC=F", days=30)
        assert len(history) == 1

    def test_multiple_records(self):
        for i in range(5):
            insert_price("Oro", "GC=F", {
                "open": 2000 + i, "high": 2050 + i, "low": 1980 + i,
                "close": 2040 + i, "volume": 5000 + i,
                "timestamp": f"2025-01-{15 + i:02d}T10:00:00",
            })
        history = get_history("GC=F", days=30)
        assert len(history) == 5
        # Verificar orden cronologico
        assert history.index[0] < history.index[-1]


class TestGetLatestPrice:
    def test_returns_none_for_unknown_ticker(self):
        assert get_latest_price("UNKNOWN") is None

    def test_returns_most_recent(self):
        insert_price("Oro", "GC=F", {
            "open": 2000, "high": 2050, "low": 1980,
            "close": 2000, "volume": 5000,
            "timestamp": "2025-01-10T10:00:00",
        })
        insert_price("Oro", "GC=F", {
            "open": 2100, "high": 2150, "low": 2080,
            "close": 2100, "volume": 6000,
            "timestamp": "2025-01-20T10:00:00",
        })
        result = get_latest_price("GC=F")
        assert result["close"] == 2100


class TestGetHistory:
    def test_empty_history(self):
        history = get_history("UNKNOWN", days=30)
        assert history.empty

    def test_respects_limit(self):
        for i in range(10):
            insert_price("Plata", "SI=F", {
                "open": 30 + i, "high": 35 + i, "low": 28 + i,
                "close": 32 + i, "volume": 1000 + i,
                "timestamp": f"2025-01-{i + 1:02d}T10:00:00",
            })
        history = get_history("SI=F", days=5)
        assert len(history) == 5

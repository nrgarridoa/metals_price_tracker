"""
Fetcher de datos de Yahoo Finance. Modulo puro Python, SIN imports de Streamlit.
Usado por el scheduler (background) y el dashboard (foreground).
"""

import logging
import pandas as pd
import yfinance as yf
from src.config import PERIOD_INTERVALS

logger = logging.getLogger(__name__)


def _normalize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza columnas de yfinance a minusculas y maneja MultiIndex."""
    rename_map = {
        "Open": "open", "High": "high", "Low": "low",
        "Close": "close", "Adj Close": "adj_close", "Volume": "volume",
    }
    # Manejar MultiIndex (versiones nuevas de yfinance con un solo ticker)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.rename(columns=rename_map)
    # Quitar timezone del indice
    if getattr(df.index, "tz", None) is not None:
        df.index = df.index.tz_localize(None)
    return df


def fetch_current_price(ticker: str) -> dict | None:
    """
    Obtiene el ultimo precio disponible para un ticker.
    Retorna dict con keys: open, high, low, close, volume, timestamp.
    """
    try:
        df = yf.download(ticker, period="5d", interval="1d", progress=False)
        if df is None or df.empty:
            return None
        df = _normalize_columns(df)
        row = df.iloc[-1]
        return {
            "open": float(row.get("open", 0)),
            "high": float(row.get("high", 0)),
            "low": float(row.get("low", 0)),
            "close": float(row.get("close", 0)),
            "volume": int(row.get("volume", 0)),
            "timestamp": df.index[-1],
        }
    except Exception as e:
        logger.error("Error obteniendo precio actual de %s: %s", ticker, e)
        return None


def fetch_historical(ticker: str, period: str = "1mo",
                     interval: str = "1d") -> pd.DataFrame:
    """
    Descarga datos historicos OHLCV. Retorna DataFrame limpio o vacio.
    """
    try:
        df = yf.download(ticker, period=period, interval=interval, progress=False)
        if df is None or df.empty:
            return pd.DataFrame()
        df = _normalize_columns(df)
        cols = [c for c in ["open", "high", "low", "close", "adj_close", "volume"]
                if c in df.columns]
        return df[cols].sort_index()
    except Exception as e:
        logger.error("Error descargando historico de %s: %s", ticker, e)
        return pd.DataFrame()


def fetch_by_period_key(ticker: str, period_key: str) -> pd.DataFrame:
    """
    Descarga datos usando una clave de PERIOD_INTERVALS ('1D', '5D', '1M', etc.).
    Funcion principal para la vista de detalle.
    """
    config = PERIOD_INTERVALS.get(period_key, PERIOD_INTERVALS["1M"])
    return fetch_historical(ticker, period=config["period"],
                            interval=config["interval"])


def fetch_intraday_24h(ticker: str) -> pd.DataFrame:
    """
    Obtiene serie intradia densa para sparkline (~24h).
    Prueba intervalos progresivamente mas gruesos como fallback.
    """
    for interval in ["5m", "15m", "30m", "60m"]:
        df = fetch_historical(ticker, period="5d", interval=interval)
        if not df.empty and len(df) >= 50:
            if "close" not in df.columns and "adj_close" in df.columns:
                df["close"] = df["adj_close"]
            cutoff = df.index.max() - pd.Timedelta(hours=24)
            return df.loc[df.index >= cutoff, ["close"]].copy()

    # Fallback final: datos diarios
    df = fetch_historical(ticker, period="1mo", interval="1d")
    if df.empty:
        return pd.DataFrame()
    if "close" not in df.columns and "adj_close" in df.columns:
        df["close"] = df["adj_close"]
    return df[["close"]].tail(2).copy()

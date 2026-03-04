"""
Operaciones SQLite para almacenamiento de precios de metales.
Esquema expandido con OHLCV, context manager, y queries parametrizadas.
"""

import sqlite3
import logging
import os
from datetime import datetime, timezone
from contextlib import contextmanager

import pandas as pd

from src.config import DB_PATH

logger = logging.getLogger(__name__)

TABLE_NAME = "precios_metales"


@contextmanager
def get_connection():
    """Context manager para conexiones a la base de datos."""
    os.makedirs(os.path.dirname(DB_PATH) or "data", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA journal_mode=WAL")
    try:
        yield conn
    finally:
        conn.close()


def init_db():
    """Crea o actualiza la tabla de precios de metales."""
    with get_connection() as conn:
        conn.execute(f"""
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                metal TEXT NOT NULL,
                ticker TEXT NOT NULL,
                open REAL,
                high REAL,
                low REAL,
                close REAL,
                volume INTEGER,
                precio_usd REAL,
                variacion_dia REAL,
                fecha TEXT NOT NULL,
                timestamp TEXT NOT NULL,
                source TEXT DEFAULT 'yfinance',
                UNIQUE(ticker, timestamp)
            );
        """)
        conn.execute(f"""
            CREATE INDEX IF NOT EXISTS idx_ticker_fecha
            ON {TABLE_NAME}(ticker, fecha);
        """)
        conn.commit()
    logger.info("Base de datos inicializada: %s", DB_PATH)


def insert_price(metal: str, ticker: str, price_data: dict,
                 source: str = "yfinance"):
    """
    Inserta un registro de precio desde el fetcher.
    price_data debe tener: open, high, low, close, volume, timestamp
    """
    ts = price_data.get("timestamp", datetime.now(timezone.utc))
    if hasattr(ts, "isoformat"):
        ts = ts.isoformat()
    fecha = ts[:10]

    with get_connection() as conn:
        try:
            conn.execute(f"""
                INSERT OR REPLACE INTO {TABLE_NAME}
                (metal, ticker, open, high, low, close, volume,
                 precio_usd, variacion_dia, fecha, timestamp, source)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, NULL, ?, ?, ?)
            """, (
                metal, ticker,
                price_data.get("open"),
                price_data.get("high"),
                price_data.get("low"),
                price_data.get("close"),
                price_data.get("volume"),
                price_data.get("close"),  # precio_usd = close
                fecha, ts, source
            ))
            conn.commit()
        except sqlite3.IntegrityError:
            logger.debug("Registro duplicado omitido: %s en %s", ticker, ts)


def get_latest_price(ticker: str) -> dict | None:
    """Obtiene el registro mas reciente para un ticker."""
    with get_connection() as conn:
        row = conn.execute(f"""
            SELECT metal, ticker, open, high, low, close, volume,
                   precio_usd, fecha, timestamp, source
            FROM {TABLE_NAME}
            WHERE ticker = ?
            ORDER BY timestamp DESC LIMIT 1
        """, (ticker,)).fetchone()
    if row is None:
        return None
    return {
        "metal": row[0], "ticker": row[1],
        "open": row[2], "high": row[3], "low": row[4],
        "close": row[5], "volume": row[6],
        "precio_usd": row[7], "fecha": row[8],
        "timestamp": row[9], "source": row[10],
    }


def get_history(ticker: str, days: int = 30) -> pd.DataFrame:
    """Obtiene registros historicos de un ticker desde la BD."""
    with get_connection() as conn:
        df = pd.read_sql_query(f"""
            SELECT fecha, open, high, low, close, volume, timestamp
            FROM {TABLE_NAME}
            WHERE ticker = ?
            ORDER BY timestamp DESC
            LIMIT ?
        """, conn, params=(ticker, days))
    if not df.empty:
        df["timestamp"] = pd.to_datetime(df["timestamp"])
        df = df.set_index("timestamp").sort_index()
    return df


def get_all_latest() -> pd.DataFrame:
    """Obtiene el ultimo registro de cada ticker."""
    with get_connection() as conn:
        df = pd.read_sql_query(f"""
            SELECT metal, ticker, close as precio_usd, fecha, timestamp
            FROM {TABLE_NAME}
            WHERE timestamp IN (
                SELECT MAX(timestamp) FROM {TABLE_NAME} GROUP BY ticker
            )
            ORDER BY metal
        """, conn)
    return df

"""
Configuracion central del Metals Price Tracker.
Tickers, periodos, y constantes configurables via .env
"""

import os
from dotenv import load_dotenv

load_dotenv()

# --- Metal Tickers (Yahoo Finance) ---
METAL_TICKERS = {
    # Metales preciosos (Futuros)
    "Oro": "GC=F",
    "Plata": "SI=F",
    "Platino": "PL=F",
    "Paladio": "PA=F",
    # Metales base / industriales (Futuros y ETFs)
    "Cobre": "HG=F",
    "Aluminio": "JJU",
    "Plomo": "LP=F",
    "Niquel": "JJN",
    "Zinc": "JJZ",
    "Estano": "TN=F",
    "Hierro": "TIO=F",
    # Metales estrategicos (ETFs)
    "Litio (ETF)": "LIT",
    "Uranio": "URA",
    "Tierras Raras": "REMX",
}

# --- Periodos para vista de detalle ---
PERIOD_INTERVALS = {
    "1D":  {"period": "1d",  "interval": "5m",  "label": "Dia"},
    "5D":  {"period": "5d",  "interval": "1h",  "label": "Semana"},
    "1M":  {"period": "1mo", "interval": "1d",  "label": "Mes"},
    "3M":  {"period": "3mo", "interval": "1d",  "label": "Trimestre"},
    "6M":  {"period": "6mo", "interval": "1d",  "label": "Semestre"},
    "1Y":  {"period": "1y",  "interval": "1d",  "label": "Ano"},
    "5Y":  {"period": "5y",  "interval": "1wk", "label": "5 Anos"},
    "10Y": {"period": "10y", "interval": "1mo", "label": "10 Anos"},
    "MAX": {"period": "max", "interval": "1mo", "label": "Todo"},
}

# --- Scheduler ---
SCHEDULER_INTERVAL_MARKET_MIN = int(os.getenv("SCHEDULER_INTERVAL_MARKET", "15"))
SCHEDULER_INTERVAL_OFF_MIN = int(os.getenv("SCHEDULER_INTERVAL_OFF", "60"))

# --- Database ---
DB_PATH = os.getenv("DB_PATH", "data/metals.db")

# --- Cache ---
CACHE_TTL_LIVE = int(os.getenv("YF_CACHE_TTL", "120"))
CACHE_TTL_HISTORICAL = 43200  # 12 horas

# --- Logging ---
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "logs/scraper.log")

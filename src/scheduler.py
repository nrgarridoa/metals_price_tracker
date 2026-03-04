"""
Scheduler basado en APScheduler para recoleccion automatica de precios.
Corre en background mientras Streamlit sirve el dashboard.
"""

import logging
from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

from src.config import (
    METAL_TICKERS,
    SCHEDULER_INTERVAL_MARKET_MIN,
    SCHEDULER_INTERVAL_OFF_MIN,
)
from src.fetcher import fetch_current_price
from src.database import insert_price, init_db

logger = logging.getLogger(__name__)

scheduler = BackgroundScheduler()


def _is_market_hours() -> bool:
    """Verifica si estamos en horario aproximado de mercado (14:30-21:00 UTC, Lun-Vie)."""
    now = datetime.utcnow()
    if now.weekday() >= 5:
        return False
    return 14 <= now.hour < 21


def fetch_all_metals():
    """Ciclo completo: obtiene precio actual de cada metal y lo guarda en BD."""
    logger.info("Scheduler: Iniciando ciclo de fetch - %s",
                datetime.utcnow().isoformat())
    success, fail = 0, 0

    for metal_name, ticker in METAL_TICKERS.items():
        try:
            price_data = fetch_current_price(ticker)
            if price_data:
                insert_price(metal_name, ticker, price_data)
                success += 1
            else:
                logger.warning("Sin datos para %s (%s)", metal_name, ticker)
                fail += 1
        except Exception as e:
            logger.error("Fallo al obtener %s (%s): %s", metal_name, ticker, e)
            fail += 1

    logger.info("Ciclo completado: %d exitosos, %d fallidos", success, fail)


def start_scheduler():
    """Inicia el scheduler en background con intervalo adaptativo."""
    init_db()

    # Fetch inicial inmediato
    fetch_all_metals()

    # Determinar intervalo segun horario de mercado
    interval_min = (SCHEDULER_INTERVAL_MARKET_MIN if _is_market_hours()
                    else SCHEDULER_INTERVAL_OFF_MIN)

    scheduler.add_job(
        fetch_all_metals,
        trigger=IntervalTrigger(minutes=interval_min),
        id="metal_fetch",
        name="Fetch precios de metales",
        replace_existing=True,
    )
    scheduler.start()
    logger.info("Scheduler iniciado con intervalo de %d minutos", interval_min)


def stop_scheduler():
    """Detiene el scheduler de forma segura."""
    if scheduler.running:
        scheduler.shutdown(wait=False)
        logger.info("Scheduler detenido")

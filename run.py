"""
Entry point: inicia el scheduler en background y lanza Streamlit.
Uso: python run.py
"""

import os
import sys
import logging
import subprocess

from src.config import LOG_LEVEL, LOG_FILE
from src.scheduler import start_scheduler, stop_scheduler


def setup_logging():
    """Configura logging a archivo y consola."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    logging.basicConfig(
        level=getattr(logging, LOG_LEVEL, logging.INFO),
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding="utf-8"),
            logging.StreamHandler(sys.stdout),
        ],
    )


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    logger.info("Iniciando Metals Price Tracker...")

    # Iniciar scheduler en background
    start_scheduler()
    logger.info("Scheduler activo. Lanzando Streamlit...")

    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run",
            "app/Home.py",
            "--server.port=8501",
        ])
    except KeyboardInterrupt:
        logger.info("Apagando...")
    finally:
        stop_scheduler()
        logger.info("Metals Price Tracker detenido.")


if __name__ == "__main__":
    main()

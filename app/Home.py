"""
Home.py -- Dashboard principal del Metals Price Tracker.
Entry point para Streamlit: streamlit run app/Home.py
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import streamlit as st
import pandas as pd
from datetime import datetime

from src.config import METAL_TICKERS, CACHE_TTL_LIVE
from src.fetcher import fetch_historical, fetch_intraday_24h
from src.database import get_latest_price
from app.components.header import render_header
from app.components.metal_table import render_metal_table

# --- Configuracion de pagina ---
st.set_page_config(
    page_title="Metals Price Tracker",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Cargar CSS ---
css_path = os.path.join(os.path.dirname(__file__), "static", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Header ---
render_header()


# --- Carga de datos con fallback a BD ---
@st.cache_data(ttl=CACHE_TTL_LIVE)
def load_all_metals():
    """Carga datos de todos los metales. Si yfinance falla, usa la BD como respaldo."""
    data_list = []

    for nombre, ticker in METAL_TICKERS.items():
        try:
            df_daily = fetch_historical(ticker, period="1mo", interval="1d")

            if df_daily.empty:
                db_record = get_latest_price(ticker)
                if db_record and db_record.get("close"):
                    data_list.append({
                        "Metal": nombre,
                        "Ticker": ticker,
                        "Precio (USD)": f"{db_record['close']:.2f}",
                        "Variacion_num": 0.0,
                        "Cambio %": "N/A",
                        "SparkDF": pd.DataFrame(),
                        "PrevClose": db_record["close"],
                    })
                continue

            if "adj_close" in df_daily.columns:
                df_daily["close_final"] = df_daily["adj_close"]
            else:
                df_daily["close_final"] = df_daily["close"]

            df_daily = df_daily.sort_index()
            primer = float(df_daily["close_final"].iloc[0])
            ultimo = float(df_daily["close_final"].iloc[-1])
            var_abs = ultimo - primer
            var_pct = (var_abs / primer) * 100 if primer else 0.0

            spark_df = fetch_intraday_24h(ticker)
            prev_close = (float(df_daily["close_final"].iloc[-2])
                          if len(df_daily) > 1 else ultimo)

            data_list.append({
                "Metal": nombre,
                "Ticker": ticker,
                "Precio (USD)": f"{ultimo:,.2f}",
                "Variacion_num": var_abs,
                "Cambio %": f"{var_pct:+.2f}%",
                "SparkDF": spark_df,
                "PrevClose": prev_close,
            })

        except Exception as e:
            st.warning(f"Error con {nombre}: {e}")
            continue

    return data_list


# --- Render principal ---
metales_data = load_all_metals()

if metales_data:
    render_metal_table(metales_data)
else:
    st.error("No se pudieron cargar datos de ningun metal. Verifica tu conexion a internet.")

# --- Footer ---
st.markdown(
    f"""
    <div class="footer">
        <p class="footer-meta">
            Actualizado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}
            &middot; Refresh cada {CACHE_TTL_LIVE}s
            &middot; {len(METAL_TICKERS)} metales
        </p>
        <p class="footer-author">
            Desarrollado por <strong>Nilson R. Garrido Asenjo</strong>
            &middot;
            <a href="https://nrgarridoa.github.io" target="_blank">nrgarridoa.github.io</a>
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

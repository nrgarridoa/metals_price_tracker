"""
1_Detalle.py -- Vista de detalle individual para cada metal.
"""

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

import streamlit as st
import pandas as pd
from datetime import datetime

from src.config import PERIOD_INTERVALS, METAL_TICKERS, CACHE_TTL_LIVE
from src.fetcher import fetch_by_period_key
from src.utils import infer_granularity
from src.database import get_latest_price
from app.components.charts import price_chart

# --- Configuracion ---
st.set_page_config(page_title="Detalle del Metal", layout="wide")

# --- Cargar CSS ---
css_path = os.path.join(os.path.dirname(__file__), "..", "static", "styles.css")
if os.path.exists(css_path):
    with open(css_path) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# --- Obtener ticker ---
ticker = st.session_state.get("selected_ticker",
                               st.query_params.get("metal", "GC=F"))
metal_name = st.session_state.get("selected_metal", "")

if not metal_name:
    for name, t in METAL_TICKERS.items():
        if t == ticker:
            metal_name = name
            break
    else:
        metal_name = ticker

# --- Boton volver (arriba) ---
col_back, col_spacer = st.columns([1, 5])
with col_back:
    st.markdown('<div class="back-btn">', unsafe_allow_html=True)
    if st.button("← Dashboard", key="back_top"):
        st.switch_page("Home.py")
    st.markdown('</div>', unsafe_allow_html=True)

# --- Obtener datos (primero, para mostrar precio antes del chart) ---
selected_period = st.session_state.get("selected_period", "3M")

@st.cache_data(ttl=CACHE_TTL_LIVE)
def load_detail_data(tkr: str, period: str):
    return fetch_by_period_key(tkr, period)

df = load_detail_data(ticker, selected_period)

if df.empty:
    db_record = get_latest_price(ticker)
    if db_record:
        st.info(f"Mostrando ultimo dato disponible de la base de datos ({db_record['fecha']})")
        st.metric("Ultimo precio", f"{db_record['close']:.2f} USD")
    else:
        st.warning("No se encontraron datos para este periodo.")
    st.stop()

# --- Datos clave ---
ultimo = df.iloc[-1]
primero = df.iloc[0]
variacion = float(ultimo["close"]) - float(primero["close"])
variacion_pct = (variacion / float(primero["close"])) * 100 if float(primero["close"]) else 0
var_class = "detail-var-positive" if variacion >= 0 else "detail-var-negative"
arrow = "&#9650;" if variacion >= 0 else "&#9660;"
granularidad = infer_granularity(df)

# --- Price header ---
st.markdown(
    f"""
    <div class="detail-price-section">
        <p class="detail-metal-title">
            {metal_name}
            <span class="ticker-badge">{ticker}</span>
        </p>
        <p class="detail-price">
            {float(ultimo['close']):,.2f}
            <span class="detail-price-currency">USD</span>
        </p>
        <p class="detail-variation {var_class}">
            {arrow} {variacion:+,.2f} ({variacion_pct:+.2f}%)
        </p>
        <p class="detail-meta">
            {df.index[-1].strftime('%d %b %Y %H:%M')}
            &middot; {granularidad or 'N/A'}
            &middot; {selected_period}
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

# --- Period selector + Chart type (juntos encima del grafico) ---
col_periods, col_chart_type = st.columns([3, 1])

with col_periods:
    period_keys = list(PERIOD_INTERVALS.keys())
    default_idx = period_keys.index(selected_period) if selected_period in period_keys else 2
    new_period = st.pills(
        "Periodo",
        period_keys,
        default=period_keys[default_idx],
        key="period_pills",
        label_visibility="collapsed",
    )
    if new_period and new_period != selected_period:
        st.session_state["selected_period"] = new_period
        st.rerun()

with col_chart_type:
    chart_type = st.pills(
        "Tipo",
        ["Montana", "Linea", "Vela"],
        default="Montana",
        key="chart_type_pills",
        label_visibility="collapsed",
    )
    if not chart_type:
        chart_type = "Montana"

# --- Chart ---
fig = price_chart(df, chart_type, ticker)
st.plotly_chart(fig, use_container_width=True)

# --- Market info cards ---
st.markdown(
    "<h3 class='section-title' style='margin-top:1rem'>Informacion del Mercado</h3>",
    unsafe_allow_html=True,
)

col1, col2, col3, col4 = st.columns(4)

vol = ultimo.get("volume", 0)
prev_close = f"{float(df['close'].iloc[-2]):,.2f}" if len(df) > 1 else "N/A"

with col1:
    st.markdown(
        f"""<div class="market-info-card">
            <div class="market-info-label">Apertura</div>
            <div class="market-info-value">{float(primero['open']):,.2f}</div>
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""<div class="market-info-card">
            <div class="market-info-label">Cierre previo</div>
            <div class="market-info-value">{prev_close}</div>
        </div>""",
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        f"""<div class="market-info-card">
            <div class="market-info-label">Maximo</div>
            <div class="market-info-value">{float(df['high'].max()):,.2f}</div>
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""<div class="market-info-card">
            <div class="market-info-label">Minimo</div>
            <div class="market-info-value">{float(df['low'].min()):,.2f}</div>
        </div>""",
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        f"""<div class="market-info-card">
            <div class="market-info-label">Volumen</div>
            <div class="market-info-value">{f'{int(vol):,}' if vol else 'N/A'}</div>
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""<div class="market-info-card">
            <div class="market-info-label">Variacion</div>
            <div class="market-info-value" style="color:{'#3FB950' if variacion >= 0 else '#F85149'}">
                {variacion:+,.2f} ({variacion_pct:+.2f}%)
            </div>
        </div>""",
        unsafe_allow_html=True,
    )

with col4:
    st.markdown(
        f"""<div class="market-info-card">
            <div class="market-info-label">Granularidad</div>
            <div class="market-info-value">{granularidad or 'N/A'}</div>
        </div>""",
        unsafe_allow_html=True,
    )
    st.markdown(
        f"""<div class="market-info-card">
            <div class="market-info-label">Ultima actualizacion</div>
            <div class="market-info-value" style="font-size:13px">{df.index[-1].strftime('%d/%m/%Y %H:%M')}</div>
        </div>""",
        unsafe_allow_html=True,
    )

# --- Tabs ---
st.markdown("<div style='height:1rem'></div>", unsafe_allow_html=True)

tab_resumen, tab_historico, tab_futuros = st.tabs(
    ["Resumen", "Datos historicos", "Futuros"]
)

with tab_resumen:
    st.dataframe(
        df.tail(10).style.format({
            "open": "{:,.2f}", "high": "{:,.2f}", "low": "{:,.2f}",
            "close": "{:,.2f}", "volume": "{:,.0f}",
        }),
        use_container_width=True,
    )

with tab_historico:
    date_col1, date_col2 = st.columns(2)
    with date_col1:
        start_date = st.date_input("Desde", df.index.min().date())
    with date_col2:
        end_date = st.date_input("Hasta", df.index.max().date())

    df_filtered = df.loc[str(start_date):str(end_date)]
    st.dataframe(df_filtered, use_container_width=True)

    st.download_button(
        label="Descargar CSV",
        data=df_filtered.to_csv().encode("utf-8"),
        file_name=f"{ticker.replace('=', '_')}_historico.csv",
        mime="text/csv",
    )

with tab_futuros:
    st.info("Proximamente: cadena de futuros de contratos asociados (GCZ25, GCM26, etc.)")

"""Componente de tabla de precios de metales."""

import streamlit as st
import pandas as pd
from app.components.charts import sparkline_24h


def render_metal_table(metales_data: list):
    """Renderiza la tabla principal de cotizaciones con sparklines."""
    st.markdown(
        "<h3 class='section-title'>Cotizaciones Actuales</h3>",
        unsafe_allow_html=True,
    )

    # Encabezados con HTML para control preciso
    st.markdown(
        """
        <div class="table-header">
            <span style="flex:2">METAL</span>
            <span style="flex:1.2; text-align:right">PRECIO (USD)</span>
            <span style="flex:1; text-align:right">VARIACION</span>
            <span style="flex:0.8; text-align:right">%</span>
            <span style="flex:2.5; text-align:center">VAR. 24H</span>
            <span style="flex:1; text-align:center"></span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Filas de datos
    for data in metales_data:
        cols = st.columns([2, 1.2, 1, 0.8, 2.5, 1])

        # Metal + Ticker
        cols[0].markdown(
            f"<div style='padding:2px 0'>"
            f"<span class='metal-name'>{data['Metal']}</span>"
            f"<br><span class='ticker'>{data['Ticker']}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Precio
        cols[1].markdown(
            f"<div style='text-align:right; padding-top:6px'>"
            f"<span class='price'>{data['Precio (USD)']}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Variacion y porcentaje
        var_num = data["Variacion_num"]
        if var_num > 0:
            symb = "&#9650;"
            css_class = "var-positive"
        elif var_num < 0:
            symb = "&#9660;"
            css_class = "var-negative"
        else:
            symb = "&mdash;"
            css_class = "var-neutral"

        cols[2].markdown(
            f"<div style='text-align:right; padding-top:6px'>"
            f"<span class='{css_class}'>{symb} {var_num:+.2f}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

        cols[3].markdown(
            f"<div style='text-align:right; padding-top:6px'>"
            f"<span class='{css_class}'>{data['Cambio %']}</span>"
            f"</div>",
            unsafe_allow_html=True,
        )

        # Sparkline 24h
        cols[4].plotly_chart(
            sparkline_24h(data.get("SparkDF", pd.DataFrame()),
                          data.get("PrevClose", 0)),
            use_container_width=True,
        )

        # Boton de detalle
        if cols[5].button("Detalle →", key=f"btn_{data['Ticker']}"):
            st.session_state["selected_ticker"] = data["Ticker"]
            st.session_state["selected_metal"] = data["Metal"]
            st.switch_page("pages/1_Detalle.py")

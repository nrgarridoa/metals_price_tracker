"""Componente de header reutilizable para el dashboard."""

import streamlit as st


def render_header():
    """Renderiza el header principal del dashboard."""
    st.markdown(
        """
        <style>.block-container {padding-top: 0 !important;}</style>
        <div class="header-container">
            <div class="header-left">
                <div>
                    <h1 class="header-title">Metals Price Tracker</h1>
                    <p class="header-subtitle">
                        Datos en tiempo real &middot; Yahoo Finance
                        &nbsp;&nbsp;
                        <span class="scheduler-status scheduler-active">
                            <span class="scheduler-dot"></span> LIVE
                        </span>
                    </p>
                </div>
            </div>
            <div class="header-right">
                <div class="header-author-text">
                    <span class="header-name">NILSON R. GARRIDO ASENJO</span>
                    <a class="header-link" href="https://nrgarridoa.github.io" target="_blank">
                        nrgarridoa.github.io
                    </a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

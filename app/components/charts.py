"""Componentes de graficos para el dashboard (sparklines, etc.)."""

import numpy as np
import pandas as pd
import plotly.graph_objects as go


# Color palette aligned with the new theme
GREEN = "#3FB950"
RED = "#F85149"
TEXT_SECONDARY = "#7D8590"
GRID_COLOR = "rgba(139, 148, 158, 0.06)"


def sparkline_24h(spark_df: pd.DataFrame, prev_close: float) -> go.Figure:
    """
    Sparkline de variacion 24h con color dinamico.
    Verde para subida, rojo para bajada.
    """
    if spark_df.empty or "close" not in spark_df.columns or prev_close is None:
        fig = go.Figure()
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
            height=60,
            xaxis=dict(visible=False),
            yaxis=dict(visible=False),
        )
        return fig

    df = spark_df.copy()
    df["variacion_pct"] = (df["close"] - prev_close) / prev_close * 100

    fig = go.Figure()

    # Baseline
    fig.add_trace(go.Scatter(
        x=df.index, y=np.zeros(len(df)),
        mode="lines",
        line=dict(color="rgba(139,148,158,0.2)", width=1, dash="dot"),
        hoverinfo="skip", showlegend=False
    ))

    # Positive
    pos = df["variacion_pct"].where(df["variacion_pct"] > 0)
    fig.add_trace(go.Scatter(
        x=df.index, y=pos, mode="lines",
        line=dict(color=GREEN, width=1.5),
        fill="tozeroy", fillcolor="rgba(63,185,80,0.1)",
        hovertemplate="%{x|%H:%M}: %{y:.2f}%<extra></extra>",
        showlegend=False
    ))

    # Negative
    neg = df["variacion_pct"].where(df["variacion_pct"] < 0)
    fig.add_trace(go.Scatter(
        x=df.index, y=neg, mode="lines",
        line=dict(color=RED, width=1.5),
        fill="tozeroy", fillcolor="rgba(248,81,73,0.1)",
        hovertemplate="%{x|%H:%M}: %{y:.2f}%<extra></extra>",
        showlegend=False
    ))

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        height=60,
        template="plotly_dark",
        hoverlabel=dict(
            bgcolor="#161B22",
            bordercolor="rgba(139,148,158,0.2)",
            font=dict(size=11, color="#E6EDF3"),
        ),
    )
    return fig


def price_chart(df: pd.DataFrame, chart_type: str = "Montana",
                ticker: str = "") -> go.Figure:
    """
    Grafico principal de precios para la vista de detalle.
    Soporta: Montana (area), Linea, Vela (candlestick).
    """
    fig = go.Figure()

    if chart_type == "Vela":
        fig.add_trace(go.Candlestick(
            x=df.index,
            open=df["open"],
            high=df["high"],
            low=df["low"],
            close=df["close"],
            name="Precio",
            increasing_line_color=GREEN,
            increasing_fillcolor="rgba(63,185,80,0.3)",
            decreasing_line_color=RED,
            decreasing_fillcolor="rgba(248,81,73,0.3)",
        ))
    else:
        # Color based on trend
        if len(df) >= 2:
            trend_color = GREEN if df["close"].iloc[-1] >= df["close"].iloc[0] else RED
        else:
            trend_color = "#58A6FF"

        rgb = ",".join(str(int(trend_color[i:i+2], 16)) for i in (1, 3, 5))

        fig.add_trace(go.Scatter(
            x=df.index,
            y=df["close"],
            mode="lines",
            fill="tozeroy" if chart_type == "Montana" else None,
            line=dict(color=trend_color, width=2),
            fillcolor=f"rgba({rgb},0.06)" if chart_type == "Montana" else None,
            name="Cierre",
            hovertemplate="%{x|%d %b %Y}<br>$%{y:,.2f}<extra></extra>",
        ))

    fig.update_layout(
        template="plotly_dark",
        height=450,
        margin=dict(l=0, r=0, t=10, b=30),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(
            gridcolor=GRID_COLOR,
            linecolor="rgba(139,148,158,0.1)",
            tickfont=dict(size=11, color=TEXT_SECONDARY),
            showgrid=True,
        ),
        yaxis=dict(
            gridcolor=GRID_COLOR,
            linecolor="rgba(139,148,158,0.1)",
            tickfont=dict(size=11, color=TEXT_SECONDARY),
            tickprefix="$",
            showgrid=True,
            side="right",
        ),
        hoverlabel=dict(
            bgcolor="#161B22",
            bordercolor="rgba(139,148,158,0.2)",
            font=dict(size=12, color="#E6EDF3"),
        ),
        xaxis_rangeslider_visible=False,
        showlegend=False,
    )
    return fig

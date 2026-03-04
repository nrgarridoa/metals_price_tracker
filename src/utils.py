"""
Funciones utilitarias puras. Sin imports de Streamlit ni fuentes de datos.
"""


def infer_granularity(df) -> str | None:
    """Determina la granularidad temporal del indice de un DataFrame."""
    if df.empty or len(df) < 2:
        return None
    delta = (df.index[1] - df.index[0]).total_seconds()
    if delta < 60:
        return "segundos"
    elif delta < 3600:
        return "minutos"
    elif delta < 86400:
        return "horas"
    elif delta < 604800:
        return "dias"
    elif delta < 2592000:
        return "semanas"
    else:
        return "meses"

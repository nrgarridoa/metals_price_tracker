# Metals Price Tracker - Data Pipeline

Pipeline automatizado para extraer, almacenar y visualizar precios de metales en tiempo real.

## Tecnologias

- **Python 3.12** - Backend
- **Streamlit** - Dashboard interactivo
- **Plotly** - Graficos avanzados (velas, sparklines)
- **yfinance** - Fuente de datos (Yahoo Finance)
- **APScheduler** - Scraping automatico en background
- **SQLite** - Almacenamiento historico local
- **Docker** - Deployment containerizado

## Arquitectura

```
[APScheduler]  -->  [Yahoo Finance API]  -->  [SQLite DB]
     (cada 15 min)                              |
                                                v
                                    [Streamlit Dashboard]
                                     |               |
                                  [Home.py]    [1_Detalle.py]
                                  (tabla +      (graficos +
                                  sparklines)    metricas)
```

## Metales Soportados (14)

| Tipo | Metal | Ticker |
|------|-------|--------|
| Precioso | Oro, Plata, Platino, Paladio | GC=F, SI=F, PL=F, PA=F |
| Industrial | Cobre, Aluminio, Plomo, Niquel, Zinc, Estano, Hierro | HG=F, JJU, LP=F, JJN, JJZ, TN=F, TIO=F |
| Estrategico | Litio, Uranio, Tierras Raras | LIT, URA, REMX |

## Inicio Rapido

```bash
# 1. Clonar e instalar
git clone <repo-url>
cd 3_Scrapping-metales
python -m venv _metales
source _metales/bin/activate  # Windows: _metales\Scripts\activate
pip install -r requirements.txt

# 2. Ejecutar (scheduler + dashboard)
python run.py

# 3. Abrir en navegador
# http://localhost:8501
```

## Con Docker

```bash
docker compose up --build
# Abrir http://localhost:8501
```

## Estructura del Proyecto

```
├── run.py                    # Entry point (scheduler + streamlit)
├── app/
│   ├── Home.py               # Dashboard principal
│   ├── pages/1_Detalle.py    # Vista detalle por metal
│   ├── components/           # Componentes reutilizables
│   └── static/styles.css     # Estilos dark theme
├── src/
│   ├── config.py             # Configuracion centralizada
│   ├── fetcher.py            # Yahoo Finance (sin Streamlit)
│   ├── scheduler.py          # APScheduler automatico
│   ├── database.py           # SQLite con esquema OHLCV
│   └── utils.py              # Utilidades puras
├── data/metals.db            # Base de datos historica
├── tests/                    # Tests unitarios
├── Dockerfile                # Deploy containerizado
└── docker-compose.yml
```

## Tests

```bash
pytest tests/ -v
```

## Configuracion (.env)

```env
YF_CACHE_TTL=120              # Cache del dashboard (seg)
SCHEDULER_INTERVAL_MARKET=15  # Intervalo en mercado (min)
SCHEDULER_INTERVAL_OFF=60     # Intervalo fuera de mercado (min)
DB_PATH=data/metals.db        # Ruta de la BD
LOG_LEVEL=INFO                # Nivel de logging
```

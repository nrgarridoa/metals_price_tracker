# Metals Price Tracker

Dashboard en tiempo real que rastrea el precio de **14 metales** (preciosos, industriales y estratégicos) con datos de Yahoo Finance.

### [▶ Ver la app en vivo](https://metalspricetracker.streamlit.app/)

---

## Capturas

| Dashboard principal | Vista detalle |
|:---:|:---:|
| ![Home](docs/screenshots/home.png) | ![Detalle](docs/screenshots/detail.png) |

## Qué puedes hacer

- **Consultar precios actuales** de oro, plata, platino, cobre, litio, uranio y 8 metales más
- **Ver sparklines** de tendencia de cada metal en los últimos 30 días
- **Explorar gráficos interactivos** con velas japonesas (candlestick) para cada metal
- **Cambiar el período** de análisis: 1 día, 5 días, 1 mes, 6 meses, 1 año o 5 años
- **Comparar métricas**: precio actual, máximo, mínimo, variación porcentual y volumen

## Metales disponibles

| Preciosos | Industriales | Estratégicos |
|-----------|-------------|-------------|
| Oro | Cobre | Litio (ETF) |
| Plata | Aluminio | Uranio |
| Platino | Plomo | Tierras Raras |
| Paladio | Níquel | |
| | Zinc | |
| | Estaño | |
| | Hierro | |

## Tecnologías

- **Streamlit** — Dashboard interactivo
- **Plotly** — Gráficos de velas y sparklines
- **yfinance** — Datos en tiempo real desde Yahoo Finance
- **SQLite** — Almacenamiento histórico local
- **APScheduler** — Actualización automática en segundo plano
- **Docker** — Deployment containerizado

---

## Instalación local

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/3_Metals_Price_Tracker.git
cd 3_Metals_Price_Tracker

# Crear entorno virtual e instalar dependencias
python -m venv _metales
source _metales/bin/activate  # Windows: _metales\Scripts\activate
pip install -r requirements.txt

# Ejecutar
python run.py
# Abrir http://localhost:8501
```

### Con Docker

```bash
docker compose up --build
# Abrir http://localhost:8501
```

## Estructura del proyecto

```
├── run.py                    # Entry point (scheduler + streamlit)
├── app/
│   ├── Home.py               # Dashboard principal
│   ├── pages/1_Detalle.py    # Vista detalle por metal
│   ├── components/           # Componentes reutilizables
│   └── static/styles.css     # Estilos dark theme
├── src/
│   ├── config.py             # Configuración centralizada
│   ├── fetcher.py            # Cliente Yahoo Finance
│   ├── scheduler.py          # APScheduler automático
│   ├── database.py           # SQLite con esquema OHLCV
│   └── utils.py              # Utilidades
├── data/metals.db            # Base de datos histórica
├── tests/                    # Tests unitarios
├── Dockerfile
└── docker-compose.yml
```

## Configuración (.env)

```env
YF_CACHE_TTL=120              # Cache del dashboard (seg)
SCHEDULER_INTERVAL_MARKET=15  # Intervalo en mercado (min)
SCHEDULER_INTERVAL_OFF=60     # Intervalo fuera de mercado (min)
DB_PATH=data/metals.db        # Ruta de la BD
LOG_LEVEL=INFO                # Nivel de logging
```

## Tests

```bash
pytest tests/ -v
```

## Contribuir

1. Fork del repositorio
2. Crear rama: `git checkout -b feature/nueva-funcionalidad`
3. Commit: `git commit -m "Agregar nueva funcionalidad"`
4. Push: `git push origin feature/nueva-funcionalidad`
5. Abrir Pull Request

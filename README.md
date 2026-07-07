![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Plotly](https://img.shields.io/badge/Plotly-3F4F75?style=for-the-badge&logo=plotly&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white)
![Streamlit Cloud](https://img.shields.io/badge/Streamlit%20Cloud-262730?style=for-the-badge&logo=streamlit&logoColor=white)

#### Si te resulta util este proyecto, apoyalo con un [![Star](https://img.shields.io/github/stars/nrgarridoa/metals_price_tracker?style=social)](https://github.com/nrgarridoa/metals_price_tracker/stargazers) en el repositorio.

---

# Metals Price Tracker - Dashboard de Precios de Metales en Tiempo Real

> **13 metales, 3 clases de instrumento distintas: futuros que cotizan el commodity directamente, ETN atados a un subindice, y ETF de acciones mineras. El dashboard distingue cada uno con su unidad de cotizacion real y clasifica el tipo de instrumento en la propia interfaz.**

Dashboard en tiempo real que rastrea 13 metales (preciosos, industriales y
estrategicos) con datos de Yahoo Finance: precios en vivo, graficos historicos,
comparacion normalizada entre metales de distinta escala de precio, y
clasificacion de instrumentos por unidad y naturaleza (futuro directo, ETN o
ETF de acciones).

[![Ver Dashboard en Vivo](https://img.shields.io/badge/Ver%20Dashboard%20en%20Vivo-Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://metalspricetracker.streamlit.app/)
&nbsp;
![Repositorio vitrina](https://img.shields.io/badge/Repositorio-vitrina-475569?style=for-the-badge&logo=github&logoColor=white)

---

## Vista previa

### Dashboard principal - tema oscuro y claro

| Tema oscuro | Tema claro |
|:---:|:---:|
| ![Home oscuro](screenshots/home_dark.png) | ![Home claro](screenshots/home_light.png) |

### Detalle por metal, con clasificacion de instrumento

![Detalle ETF](screenshots/detalle_etf.png)

### Comparacion normalizada de metales a distinta escala de precio

![Comparar metales](screenshots/comparar.png)

---

## Que problema resuelve

| Sin este dashboard | Con este dashboard |
|---|---|
| "Precio del metal" sin distinguir futuro, ETN o ETF de acciones | Unidad real (USD/oz troy, USD/lb, USD/tonelada) y badge ETN/ETF por instrumento |
| Comparar oro (~4000 USD/oz) y plata (~60 USD/oz) en un mismo grafico deja a la de menor precio ilegible | Comparacion normalizada a variacion % desde el inicio del periodo (misma convencion que usan Yahoo Finance y TradingView) |
| El indicador de estado no distingue datos en vivo de un respaldo | Estado real: LIVE cuando Yahoo Finance responde, aviso de cache cuando se usa el respaldo local |
| Contratos de baja liquidez muestran variaciones que parecen movimiento de mercado pero son ruido de actualizacion | Se marcan como N/D en lugar de un numero que no representa el mercado |
| Un link a un metal especifico no conserva el periodo ni el tipo de grafico | Estado (metal, periodo, tipo de grafico) reflejado en la URL, compartible tal cual |

---

## Hallazgos

**Tres tickers de metales base llevaban dos anos sin cotizar**
- Los ETN de aluminio, niquel y zinc (JJU/JJN/JJZ) fueron redimidos por Barclays el 14/06/2023
- Se reemplazaron aluminio y zinc por sus futuros COMEX directos (ALI=F, ZNC=F); niquel se retiro del dashboard al no existir un futuro equivalente en Yahoo Finance

**3 de 13 instrumentos son acciones, no el commodity**
- Litio, uranio y tierras raras se obtienen via ETF de empresas mineras (Global X, VanEck) -- su precio refleja el mercado accionario del sector, no el precio spot del metal
- El dashboard los distingue con un badge ETF y la unidad de cotizacion correspondiente

**Los futuros de reemplazo tienen baja liquidez**
- Aluminio, plomo y zinc en COMEX actualizan su precio de forma espaciada en Yahoo Finance (el mismo valor puede repetirse varios dias)
- Su variacion % se marca como N/D en vez de mostrar un cambio que no corresponde a un movimiento real

---

## Metales disponibles

| Preciosos | Industriales | Estrategicos |
|-----------|-------------|-------------|
| Oro | Cobre | Litio (ETF) |
| Plata | Aluminio | Uranio (ETF) |
| Platino | Plomo | Tierras Raras (ETF) |
| Paladio | Zinc | |
| | Estano | |
| | Hierro | |

Niquel no esta disponible: no existe un futuro directo equivalente en Yahoo
Finance para reemplazar el ETN redimido en 2023 (el niquel cotiza
principalmente en la LME).

---

## Secciones del dashboard

### Cotizaciones actuales
Precio, unidad de cotizacion, variacion, sparkline de 24h y badge ETN/ETF con
tooltip por instrumento.

### Detalle por metal
Grafico interactivo (montana, linea o velas japonesas), selector de periodo de
1 dia a historico completo, tarjetas de informacion de mercado, descarga a CSV
y estado (metal, periodo, tipo de grafico) reflejado en la URL.

### Comparar metales
Seleccion de 2 a 4 metales normalizados a variacion % desde el inicio del
periodo, para comparar activos de escalas de precio muy distintas en un mismo
grafico.

### Tema claro / oscuro
Paleta completa, incluyendo los graficos de Plotly, adaptada a ambos temas.

---

## Autor

### Nilson Rolando Garrido Asenjo

**Mining Engineer | Data Analyst | Python Developer**

[![Portfolio](https://img.shields.io/badge/Portfolio-nrgarridoa.github.io-0068FF?style=for-the-badge&logo=github&logoColor=white)](https://nrgarridoa.github.io)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-nrgarridoa-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/nrgarridoa)
[![YouTube](https://img.shields.io/badge/YouTube-nrgarridoa-FF0000?style=for-the-badge&logo=youtube&logoColor=white)](https://www.youtube.com/@nrgarridoa)
[![Gmail](https://img.shields.io/badge/Gmail-nrgarridoa@gmail.com-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:nrgarridoa@gmail.com)

Ingeniero de Minas (UNC, primer puesto) y Administrador Industrial (SENATI) con
trayectoria en gran mineria, industria farmaceutica y manufactura de alimentos.
He liderado equipos de campo en Newmont Yanacocha, Gold Fields y Silver Mountain,
dirigido proyectos tecnologicos en CODE UNI y ejecutado consultoria de
reconciliacion de mineral para Chinalco y desarrollo de reporteria de seguridad
operativa (monitoreo de fatiga y somnolencia de flota) para Antamina.

Mi enfoque es transformar datos operativos en inteligencia para la toma de
decisiones, combinando experiencia de campo con herramientas como Power BI,
Python, SQL y DAX. Piloto de drones con operaciones en superficie (fotogrametria,
volumetria) y en subterranea (LiDAR con Elios 3 para Flyability). Docente de
Power BI y Python aplicado a mineria.

Formacion continua en Platzi, Coursera, iSE-Latam y Netzun en analitica de datos,
programacion, gestion agil de proyectos y tecnologias mineras.

[![GitHub](https://img.shields.io/badge/GitHub-nrgarridoa-black?style=for-the-badge&logo=github&logoColor=white)](https://github.com/nrgarridoa)

---

<details>
<summary><strong>Documentacion Tecnica (clic para expandir)</strong></summary>

## Modelo de datos e instrumentos

Cada ticker esta clasificado en `src/config.py` por unidad de cotizacion real y
tipo de instrumento:

| Clase | Significado | Ejemplo |
|---|---|---|
| `direct` | Futuro que cotiza el commodity directamente | Oro (`GC=F`, USD/oz troy) |
| `etn` | ETN ligado a un subindice de futuros (roll incluido, no es 1:1 con el spot) | -- (los 3 ETN de aluminio/niquel/zinc quedaron redimidos, ver Hallazgos) |
| `equity` | ETF de acciones de empresas del sector -- el precio depende del mercado accionario | Litio (`LIT`), Uranio (`URA`), Tierras Raras (`REMX`) |

Los instrumentos `direct` de baja liquidez (aluminio, plomo, zinc) llevan
ademas un flag que hace que la interfaz muestre "N/D" en la variacion % en vez
de un numero derivado de una actualizacion espaciada.

## Arquitectura

- **Streamlit** multipagina (`Home.py` + `pages/`) con `theme.py` inyectando la
  paleta clara/oscura via variables CSS: un segundo bloque `:root{}` sobreescribe
  los tokens que cambian segun el tema de la sesion, sin JS en el cliente.
- **Plotly** para velas, sparklines y el grafico de comparacion normalizada,
  con paleta propia por tema (`plotly_dark` / `plotly_white`).
- **yfinance** como fuente de datos en vivo, con cache de Streamlit (`st.cache_data`)
  de TTL corto para vistas de corto plazo y TTL largo (12h) para periodos
  historicos que casi no cambian entre refrescos.
- **SQLite + APScheduler** para historico y respaldo local en un despliegue
  propio con almacenamiento persistente (Docker) -- Streamlit Community Cloud
  solo ejecuta la app Streamlit, asi que ahi el dashboard trabaja en vivo
  contra Yahoo Finance en cada carga.

## Stack tecnologico

| Herramienta | Uso |
|---|---|
| **Python** | Lenguaje base |
| **Streamlit** | Framework del dashboard |
| **Plotly** | Graficos interactivos (velas, sparklines, comparacion normalizada) |
| **yfinance** | Cliente de datos de Yahoo Finance |
| **Pandas** | Procesamiento de series de tiempo |
| **SQLite + APScheduler** | Historico y respaldo local (despliegue propio) |
| **pytest + GitHub Actions** | Tests automatizados y CI |
| **Docker** | Deployment containerizado alternativo |
| **Streamlit Community Cloud** | Hosting del demo en vivo |

</details>

---

## Sobre el codigo

Este es un **repositorio vitrina**: documenta la solucion y enlaza el demo en
vivo. El codigo de la aplicacion se mantiene en un repositorio privado para
proteger la implementacion. **Con gusto hago un recorrido por el codigo en una
entrevista tecnica o facilito el acceso bajo solicitud** -- escribeme por
[LinkedIn](https://www.linkedin.com/in/nrgarridoa) o
[correo](mailto:nrgarridoa@gmail.com).

---

(c) 2026 Nilson Rolando Garrido Asenjo -- Todos los derechos reservados. Ver [LICENSE](LICENSE).

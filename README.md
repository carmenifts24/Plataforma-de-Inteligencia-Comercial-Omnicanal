# RetailIQ 360° — Plataforma de Inteligencia Comercial Omnicanal

Proyecto integrador de análisis de datos con enfoque omnicanal. Integra datasets de e-commerce brasileño, retail internacional, benchmarks del comercio electrónico argentino y contexto macroeconómico para construir una plataforma de inteligencia comercial.

## Objetivo

Construir una plataforma de análisis que permita visualizar KPIs clave, detectar patrones de compra y tomar decisiones basadas en datos a través de múltiples canales de venta.

## Datasets utilizados

| Dataset | Descripción |
|---|---|
| Olist | Transacciones de e-commerce brasileño (pedidos, ítems, productos, reseñas) |
| Sample Superstore | Ventas retail multicanal — referencia de márgenes y descuentos |
| CACE | Benchmarks del comercio electrónico argentino (KPIs, conversión, logística, medios de pago) |
| IPC INDEC | Índice de precios al consumidor para ajuste por inflación |
| Tipos de cambio | Cotizaciones históricas USD/ARS — columna `dolar_estadounidense` |
| Datos sintéticos | Capa argentina generada con Faker: clientes, sucursales, canales, ventas base |

## Estructura del proyecto

```
integrador_carrera/
├── notebooks/                        # Notebooks Jupyter numerados
│   ├── 00_configuracion_entorno.ipynb
│   ├── 01_creador_datos_sinteticos.ipynb
│   ├── 02_EDA_nivel_1.ipynb          # Diagnóstico estructural por archivo
│   ├── 03_EDA_nivel_2.ipynb          # Exploración por grupo funcional
│   └── 04_ETL.ipynb                  # Integración, conversión monetaria e inflación
├── extras/                           # Explicaciones, guía GitHub y dashboard HTML
├── src/
│   └── utils.py                      # Funciones helper reutilizables
├── datos/
│   ├── 01_raw/                       # Datos originales sin modificar (no versionados)
│   ├── 02_cace_benchmarks/           # Benchmarks CACE del comercio argentino
│   ├── 03_sinteticos/                # Datos sintéticos generados (no versionados)
│   ├── 04_procesados/                # Outputs procesados: IPC y fact_ventas.csv
│   └── respaldo de datos/            # Archivos comprimidos de respaldo (no versionados)
├── diseño/                           # Diagramas del modelo de datos
├── informacion_teorica/              # Bibliografía y guías de referencia
├── docs/                             # Documentación del proyecto
├── requirements.txt
└── .gitignore
```

## Tecnologías

- **Python 3.14** — lenguaje principal
- **Pandas / NumPy** — manipulación y análisis de datos
- **Matplotlib / Seaborn / Plotly** — visualización
- **Scikit-learn** — machine learning
- **JupyterLab** — entorno de desarrollo interactivo
- **Git / GitHub** — control de versiones

## Instalación

```bash
git clone https://github.com/carmenifts24/Plataforma-de-Inteligencia-Comercial-Omnicanal.git
cd Plataforma-de-Inteligencia-Comercial-Omnicanal
pip install -r requirements.txt
jupyter lab
```

## Modelo de datos

El proyecto utiliza un **esquema galaxia** con dos tablas de hechos:
- `FactVentas` — ítems vendidos, revenue, canal, cliente y geografía
- `FactPreciosComp` — precios propios vs competencia por categoría y período

Conectadas a dimensiones compartidas: tiempo, cliente, producto, región, canal, vendedor e inflación.

## Pipeline de notebooks

| Notebook | Propósito | Resultado principal |
|----------|-----------|--------------------|
| `00_configuracion_entorno.ipynb` | Verificar entorno, librerías y lectura inicial de datos | Ambiente validado para trabajar |
| `01_creador_datos_sinteticos.ipynb` | Crear capa argentina ficticia y reproducible | Dimensiones y hechos sintéticos |
| `02_EDA_nivel_1.ipynb` | Diagnosticar calidad de cada archivo por separado | Semáforo de calidad y `dim_inflacion_ipc.csv` |
| `03_EDA_nivel_2.ipynb` | Validar relaciones entre datasets | Base preliminar de `FactVentas` y decisiones de joins |
| `04_ETL.ipynb` | Integrar ventas, convertir BRL a ARS y ajustar por inflación | `datos/04_procesados/fact_ventas.csv` |

## Documentación explicativa

La carpeta `extras/` contiene explicaciones didácticas de cada notebook para que el proyecto pueda entenderse aunque la persona no tenga experiencia en desarrollo de software:

- `00_configuracion_entorno_explicacion.md`
- `01_creador_datos_sinteticos_explicacion.md`
- `02_EDA_nivel_1_explicacion.md`
- `03_EDA_nivel_2_explicacion.md`
- `04_ETL_explicacion.md`
- `dashboard_retailiq360.html`
- `procedimiento_actualizar_repositorio_github.md`

## Estado del proyecto

| Fase | Descripción | Estado |
|------|-------------|--------|
| 0 | Configuración del entorno | ✓ Completo |
| 1 | Generación de datos sintéticos argentinos | ✓ Completo |
| 2 | EDA Nivel 1 — diagnóstico estructural por archivo | ✓ Completo |
| 3 | EDA Nivel 2 — exploración por grupo funcional | ✓ Completo |
| 4 | ETL — limpieza, integración, conversión BRL→ARS y ajuste por inflación | ✓ Completo |
| 5 | Modelado y KPIs | Pendiente |
| 6 | Dashboard explicativo y presentación final | En progreso |

## Autora

Carmen — IFTS N° 24 | Tecnicatura en Ciencia de Datos

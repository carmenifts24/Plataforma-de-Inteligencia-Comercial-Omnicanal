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
│   └── 03_EDA_nivel_2.ipynb          # Exploración por grupo funcional
├── extras/                           # Explicaciones en texto de cada notebook
├── src/
│   └── utils.py                      # Funciones helper reutilizables
├── datos/
│   ├── 01_raw/                       # Datos originales sin modificar (no versionados)
│   ├── 02_cace_benchmarks/           # Benchmarks CACE del comercio argentino
│   ├── 03_sinteticos/                # Datos sintéticos generados (no versionados)
│   ├── 04_procesados/                # Outputs del EDA listos para ETL
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

## Estado del proyecto

| Fase | Descripción | Estado |
|------|-------------|--------|
| 0 | Configuración del entorno | ✓ Completo |
| 1 | Generación de datos sintéticos argentinos | ✓ Completo |
| 2 | EDA Nivel 1 — diagnóstico estructural por archivo | ✓ Completo |
| 3 | EDA Nivel 2 — exploración por grupo funcional | ✓ Completo |
| 4 | ETL — limpieza, integración y conversión de datos | Pendiente |
| 5 | Modelado y KPIs | Pendiente |
| 6 | Dashboard y presentación final | Pendiente |

## Autora

Carmen — IFTS N° 24 | Tecnicatura en Ciencia de Datos

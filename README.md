# RetailIQ 360° - Plataforma de Inteligencia Comercial Omnicanal

Proyecto integrador de análisis de datos con enfoque omnicanal. Integra datos de e-commerce, benchmarks del comercio electrónico argentino, contexto macroeconómico y una capa sintética argentina para construir una plataforma de inteligencia comercial en Power BI.

## Objetivo

Construir una plataforma de análisis que permita visualizar KPIs clave, detectar patrones de compra y apoyar decisiones comerciales basadas en datos a través de múltiples canales de venta.

## Datasets Utilizados

| Dataset | Descripción |
|---|---|
| Olist | Transacciones de e-commerce brasileño procesadas para análisis histórico. |
| CACE | Benchmarks del comercio electrónico argentino: KPIs, conversión, logística, medios de pago, distribución regional y perfil comprador. |
| IPC INDEC | Índice de precios al consumidor usado para ajustar valores por inflación. |
| Tipos de cambio | Cotizaciones históricas para conversión monetaria. |
| Datos sintéticos | Capa argentina generada con Faker: clientes, sucursales, canales, ventas base y precios de competencia. |

## Estructura del Proyecto

```text
integrador_carrera/
├── notebooks/                         # Notebooks Jupyter numerados
│   ├── 00_configuracion_entorno.ipynb
│   ├── 01_creador_datos_sinteticos.ipynb
│   ├── 02_EDA_nivel_1.ipynb
│   ├── 03_EDA_nivel_2.ipynb
│   ├── 04_ETL.ipynb
│   ├── 05_market_basket.ipynb
│   └── 06_clustering_clientes.ipynb
├── datos/
│   ├── 02_cace_benchmarks/            # Tablas CACE de referencia
│   ├── 03_sinteticos/                 # Datos sintéticos generados
│   └── 04_procesados/                 # Outputs finales para Power BI
├── sql/                               # Esquema SQL Server del modelo de datos
├── power_bi/                          # Archivo .pbix del dashboard
├── extras/                            # Guías, explicaciones y diagramas
├── diseño/                            # Diagramas auxiliares del proyecto
├── docs/                              # Documentación final
├── src/                               # Funciones helper
├── requirements.txt
└── README.md
```

## Tecnologías

- Python
- Pandas / NumPy
- Matplotlib / Seaborn / Plotly
- Scikit-learn (K-Means, MLxtend Apriori)
- JupyterLab
- Power BI
- SQL Server
- Git / GitHub

## Instalación

```bash
git clone https://github.com/carmenifts24/Plataforma-de-Inteligencia-Comercial-Omnicanal.git
cd Plataforma-de-Inteligencia-Comercial-Omnicanal
pip install -r requirements.txt
jupyter lab
```

## Modelo de Datos en Power BI

El modelo final se organiza como un **esquema galaxia**, porque contiene más de una tabla de hechos. Cada tabla de hechos conserva su propia estrella de dimensiones.

Diagrama actualizado:

[extras/07_modelo_relaciones_estrella_galaxia.svg](extras/07_modelo_relaciones_estrella_galaxia.svg)

### Tablas de Hechos

| Tabla | Archivo | Descripción |
|---|---|---|
| `FactVentasFinal` | `04_procesados/fact_ventas_final.csv` | 110 197 transacciones Olist con precios reales en ARS, ajuste por inflación y contexto argentino sintético (canal, cliente, medio de pago, logística). Tabla principal del modelo. |
| `FactPreciosComp` | `04_procesados/fact_precios_comp.csv` | 360 filas (30 categorías × 12 meses). Precio propio, precio competencia y price index mensual por categoría. |
| `MarketBasketReglas` | `04_procesados/market_basket_reglas.csv` | Reglas de asociación filtradas (soporte, confianza, lift) para análisis de venta cruzada. |
| `MarketBasketEnriquecidas` | `04_procesados/market_basket_reglas_enriquecidas.csv` | Reglas de asociación con nombres de categorías CACE en español. |

> `005_fact_ventas_base_ar.csv` quedó deprecada: sus columnas de precio eran 100 % nulas. Su contexto argentino (CanalID, ClienteID, etc.) fue integrado directamente en `fact_ventas_final.csv`.

### Dimensiones Principales

| Tabla | Archivo | Descripción |
|---|---|---|
| `DimGeografia` | `03_sinteticos/001_dim_geografia_ar.csv` | 67 filas. Jerarquía geográfica AR: región, provincia, ciudad y zona. |
| `DimSucursalesAr` | `03_sinteticos/002_dim_sucursales_ar.csv` | 50 sucursales físicas con FK a DimGeografia. |
| `DimCanal` | `03_sinteticos/003_dim_canal_ar.csv` | 4 canales de venta: tienda física, web, app y marketplace. |
| `DimClientesAr` | `04_procesados/dim_clientes_ar.csv` | 10 000 clientes sintéticos con `GeografiaID` para filtrado geográfico directo. |
| `DimInflacionIpc` | `04_procesados/dim_inflacion_ipc.csv` | 111 meses de IPC (INDEC). Clave relacional: `PeriodoID = anio * 100 + mes`. |
| `DimTiempo` | `04_procesados/dim_tiempo.csv` | Tabla de tiempo con jerarquía año/mes/trimestre para navegación temporal en Power BI. |
| `DimCategorias` | `04_procesados/dim_categorias.csv` | Categorías de productos con nombres en español (nomenclatura CACE). |
| `DimProductos` | `04_procesados/dim_productos.csv` | Catálogo de productos con categoría asignada. |

### Tablas de Análisis Avanzado

| Tabla | Archivo | Descripción |
|---|---|---|
| `ClusteringClientes` | `04_procesados/clustering_clientes.csv` | Segmentación K-Means de 9 999 clientes en 4 clusters (Alto valor / Frecuente / Ocasional / Inactivo) con features RFM. |
| `CohortesRetencion` | `04_procesados/cohortes_retencion.csv` | Análisis de cohortes en formato largo: tasa de retención por cohorte y mes de vida. |
| `CohortesResumen` | `04_procesados/cohortes_resumen.csv` | Métricas de retención consolidadas por cohorte (mes 1, mes 3, mes 6, vida promedio). |
| `CohortesMatrizAncha` | `04_procesados/cohortes_matriz_ancha.csv` | Matriz de retención en formato ancho (mes_0 … mes_12) para formato condicional en Power BI. |

### Relaciones Formales

| Tabla lado 1 | Columna | Tabla lado * | Columna | Tipo |
|---|---|---|---|---|
| `DimGeografia` | `GeografiaID` | `DimSucursalesAr` | `GeografiaID` | Activa |
| `DimGeografia` | `GeografiaID` | `DimClientesAr` | `GeografiaID` | Activa |
| `DimCanal` | `CanalID` | `FactVentasFinal` | `CanalID` | Activa |
| `DimClientesAr` | `ClienteID` | `FactVentasFinal` | `ClienteID` | Activa |
| `DimSucursalesAr` | `SucursalID` | `FactVentasFinal` | `SucursalID` | Activa |
| `DimInflacionIpc` | `PeriodoID` | `FactVentasFinal` | `PeriodoID` | Activa |
| `DimCanal` | `CanalID` | `FactPreciosComp` | `CanalID` | Inactiva |
| `DimClientesAr` | `ClienteID` | `ClusteringClientes` | `ClienteID` | Activa |

> `SucursalID` es nulo para el 92 % de las filas (ventas online). La relación cubre sólo el canal tienda física — es comportamiento esperado del modelo.

### Tablas CACE

Las tablas `cace_*` son **benchmarks de referencia**. No deben tener relaciones formales en el modelo de Power BI. Se usan directamente en visualizaciones para comparar contra métricas propias por categoría, región, canal, medios de pago, logística o perfil comprador.

## Pipeline de Notebooks

| Notebook | Propósito | Resultado principal |
|---|---|---|
| `00_configuracion_entorno.ipynb` | Verificar entorno, librerías y lectura inicial de datos. | Ambiente validado. |
| `01_creador_datos_sinteticos.ipynb` | Crear capa argentina ficticia y reproducible calibrada con CACE. | Dimensiones y hechos sintéticos en `03_sinteticos/`. |
| `02_EDA_nivel_1.ipynb` | Diagnosticar calidad de cada archivo por separado. | Semáforo de calidad y `dim_inflacion_ipc.csv`. |
| `03_EDA_nivel_2.ipynb` | Validar relaciones entre datasets. | Decisiones de joins y análisis preliminares. |
| `04_ETL.ipynb` | Integrar ventas Olist con la capa argentina, convertir BRL→ARS, ajustar por inflación y generar todas las dimensiones del modelo. | `fact_ventas_final.csv`, `dim_clientes_ar.csv`, `dim_inflacion_ipc.csv`, `dim_tiempo.csv`, `dim_categorias.csv`, `dim_productos.csv`, `fact_precios_comp.csv`. |
| `05_market_basket.ipynb` | Descubrir patrones de compra conjunta con reglas de asociación (Apriori) a nivel categoría y producto. | `market_basket_reglas.csv`, `market_basket_reglas_enriquecidas.csv`. |
| `06_clustering_clientes.ipynb` | Segmentación no supervisada K-Means sobre features RFM + análisis de cohortes de retención. | `clustering_clientes.csv`, `cohortes_retencion.csv`, `cohortes_resumen.csv`, `cohortes_matriz_ancha.csv`. |

## Esquema SQL

`sql/retailiq360_schema.sql` contiene el DDL completo para SQL Server con todas las tablas del modelo, tipos de dato unificados, claves primarias y foráneas. Permite importar los CSV exportados por el pipeline de notebooks en una base de datos relacional para análisis adicionales.

## Documentación Explicativa

La carpeta `extras/` contiene material de apoyo para entender y presentar el proyecto:

| Archivo | Descripción |
|---|---|
| `00_configuracion_entorno_explicacion.md` | Guía narrativa del notebook 00. |
| `01_creador_datos_sinteticos_explicacion.md` | Guía narrativa del notebook 01. |
| `02_EDA_nivel_1_explicacion.md` | Guía narrativa del notebook 02. |
| `03_EDA_nivel_2_explicacion.md` | Guía narrativa del notebook 03. |
| `04_ETL_explicacion.md` | Guía narrativa del notebook 04. |
| `05_guia_tablas_power_bi.md` | Guía de carga y configuración de tablas en Power BI. |
| `06_diagrama_relaciones.html` | Diagrama interactivo de relaciones del modelo. |
| `07_modelo_relaciones_estrella_galaxia.svg` | Diagrama SVG del esquema galaxia. |
| `08_dashboard_retailiq360.html` | Dashboard explicativo completo del proyecto (HTML estático). |
| `09_generar_diccionario.py` | Script que genera el diccionario de datos en Excel. |
| `10_dashboard_validaciones_eda_etl.html` | Dashboard interactivo de validaciones del ETL y EDA. |
| `11_diagrama_de_pert_del_proyecto.html` | Diagrama PERT interactivo del proyecto. |
| `12_cronograma_interactivo_de_proyecto.html` | Cronograma interactivo de fases y tareas. |
| `13_cronograma_gantt_interactivo.html` | Diagrama de Gantt interactivo del proyecto. |
| `14_ResumenProyecto_RetailIQ360.docx` | Resumen ejecutivo del proyecto. |
| `diccionario_datos_RetailIQ360.xlsx` | Diccionario de datos completo: tablas, columnas y descripciones. |
| `CostosFinancieros_RetailIQ360.xlsx` | Análisis de costos financieros del proyecto. |
| `VAN_RetailIQ360.xlsx` | Cálculo del Valor Actual Neto (VAN) del proyecto. |
| `contexto_agente_ia.md` | Contexto del proyecto para uso con asistente de IA. |
| `procedimiento_actualizar_repositorio_github.md` | Guía paso a paso para hacer push a GitHub. |

## Estado del Proyecto

| Fase | Descripción | Estado |
|---|---|---|
| 0 | Configuración del entorno | Completo |
| 1 | Generación de datos sintéticos argentinos | Completo |
| 2 | EDA Nivel 1 | Completo |
| 3 | EDA Nivel 2 | Completo |
| 4 | ETL: integración completa, conversión BRL→ARS, ajuste por inflación, generación de dimensiones | Completo |
| 5 | Market Basket Analysis: reglas de asociación Apriori por categoría y producto | Completo |
| 6 | Clustering K-Means: segmentación RFM en 4 clusters (Alto valor / Frecuente / Ocasional / Inactivo) | Completo |
| 7 | Análisis de cohortes: retención mensual, resumen por cohorte y matriz ancha para Power BI | Completo |
| 8 | Dashboards en Power BI: fases 1 a 8 con KPIs, segmentación, cohortes y market basket | En progreso |
| 9 | Análisis financiero: VAN, costos del proyecto y documentación final | En progreso |

## Autoras

Carmen Rodríguez y Tamara Peña  
Proyecto Final Integrador  
IFTS N° 24 | Tecnicatura en Ciencia de Datos

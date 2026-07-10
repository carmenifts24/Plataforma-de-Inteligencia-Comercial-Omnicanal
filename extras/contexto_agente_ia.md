# Contexto para Agente de IA — RetailIQ 360°

> **Uso:** Este documento es el brief de contexto para que un agente de IA pueda asistir en consultas, evaluar avance y resolver conflictos en el proyecto integrador final de la Tecnicatura en Ciencia de Datos del IFTS N° 24.

---

## 1. Identificación del Proyecto

| Campo | Valor |
|-------|-------|
| **Nombre** | RetailIQ 360° — Plataforma de Inteligencia Comercial Omnicanal |
| **Equipo** | Carmen Rodríguez y Tamara Peña |
| **Institución** | IFTS N° 24 — Tecnicatura Superior en Ciencia de Datos |
| **Tipo** | Proyecto Final Integrador |
| **Repositorio** | https://github.com/carmenifts24/Plataforma-de-Inteligencia-Comercial-Omnicanal |
| **Directorio local** | `c:\Proyectos\integrador_carrera` |
| **Fecha de referencia** | Julio 2026 (defensa realizada el 06/07/2026) |

---

## 2. Objetivo General

Construir una plataforma integral de análisis que permita a una empresa de retail argentina visualizar KPIs clave, detectar patrones de compra y apoyar decisiones comerciales basadas en datos a través de tres canales de venta: **tienda física, canales digitales propios (web y app) y marketplace**.

---

## 3. Objetivos Específicos

1. Generar un conjunto de datos sintéticos representativos del mercado e-commerce argentino, calibrados con benchmarks reales (CACE 2025).
2. Aplicar un pipeline de ETL que unifique fuentes heterogéneas: datos transaccionales brasileños (Olist), contexto macroeconómico argentino (IPC INDEC, tipo de cambio BCRA) y datos sintéticos propios.
3. Construir un modelo de datos tipo galaxia en Power BI con tablas de hechos y dimensiones correctamente relacionadas.
4. Descubrir patrones de compra conjunta (Market Basket / Apriori) y segmentar clientes (K-Means sobre RFM + cohortes de retención).
5. Desarrollar un dashboard interactivo de 10 páginas que responda 8 preguntas de negocio omnicanal: ticket promedio, conversión, canales, geografía, inflación, competencia, segmentación y cross-selling.
6. Evaluar la viabilidad económica del proyecto mediante análisis de VAN y estructura de costos.

---

## 4. Stack Tecnológico

- **Lenguaje:** Python 3 con Jupyter (análisis, ETL, generación de datos, minería de datos)
- **Librerías principales:** Pandas, NumPy, Scikit-learn (K-Means), MLxtend (Apriori), Faker, Plotly, Seaborn, Matplotlib
- **BI:** Power BI Desktop + DAX, Power Query, DAX Studio (VertiPaq Analyzer)
- **Control de versiones:** Git / GitHub
- **Entorno:** Windows 11, JupyterLab

---

## 5. Fuentes de Datos

| ID | Fuente | Descripción | Rol en el proyecto |
|----|--------|-------------|-------------------|
| **Olist** | Dataset público de e-commerce brasileño (2016–2018) | 110.197 transacciones reales con órdenes, ítems, productos y reseñas | Tabla de hechos principal (ventas) |
| **CACE 2025** | Cámara Argentina de Comercio Electrónico | 11+ benchmarks: KPIs macro, categorías, medios de pago, logística, geografía | Calibración de datos sintéticos + tablas de referencia en Power BI |
| **IPC INDEC** | Índice de Precios al Consumidor (Argentina) | 111 meses de inflación mensual | Deflactar precios a pesos constantes de dic-2016 |
| **Tipos de cambio BCRA** | Banco Central de la República Argentina | Cotizaciones diarias ARS/USD históricas | Convertir precios de BRL a ARS |
| **Datos sintéticos** | Generados con Faker (SEED=42) | Clientes, sucursales, canales, medios de pago, logística — contexto argentino | Enriquecer Olist con dimensiones omnicanal argentinas |

---

## 6. Estructura del Repositorio

```
integrador_carrera/
├── notebooks/                     # Pipeline de análisis (7 notebooks numerados + 2 scripts de utilidad)
│   ├── 00_configuracion_entorno.ipynb
│   ├── 01_creador_datos_sinteticos.ipynb
│   ├── 02_EDA_nivel_1.ipynb
│   ├── 03_EDA_nivel_2.ipynb
│   ├── 04_ETL.ipynb
│   ├── 05_market_basket.ipynb
│   ├── 06_clustering_clientes.ipynb
│   ├── 07_generar_diccionario.py      # Genera extras/diccionario_datos_RetailIQ360.xlsx
│   └── 08_generar_notebook_05.py      # Utilidad de desarrollo: regenera 05_market_basket.ipynb
├── datos/
│   ├── 01_raw/                    # Datos originales sin modificar (Olist, IPC, BCRA, Superstore)
│   ├── 02_cace_benchmarks/        # Tablas CACE de referencia
│   ├── 03_sinteticos/             # Tablas generadas por notebook 01
│   └── 04_procesados/             # Salidas finales para Power BI
├── power_bi/                       # Archivo .pbix del dashboard (10 páginas)
├── extras/                         # Documentación narrativa, guías y diagramas
├── docs/                           # Documentación y presentación final de defensa
├── src/                             # Funciones helper reutilizables
└── requirements.txt
```

---

## 7. Pipeline de Notebooks

### Notebook 00 — Configuración del Entorno
Verifica versiones de librerías, configura estilos visuales e inventaría los archivos de datos disponibles. **Estado: Completo.**

### Notebook 01 — Creador de Datos Sintéticos
Genera 6 tablas con SEED=42 para reproducibilidad: `001_dim_geografia_ar.csv` (67 filas), `002_dim_sucursales_ar.csv` (50 sucursales), `003_dim_canal_ar.csv` (4 canales con pesos CACE), `dim_clientes_ar.csv` (10.000 clientes), `fact_ventas_base_ar.csv` (150.000 filas, deprecada), `006_fact_precios_comp.csv` (360 precios de competencia). **Estado: Completo.**

### Notebook 02 — EDA Nivel 1
Diagnóstico individual de cada dataset (nulos, duplicados, tipos, estadísticas). Genera `dim_inflacion_ipc.csv`. Decisión clave: usar solo órdenes Olist con estado "delivered". **Estado: Completo.**

### Notebook 03 — EDA Nivel 2
Valida integridad referencial entre datasets, cobertura temporal IPC vs. ventas, y mapea categorías Olist a categorías CACE en español. **Estado: Completo.**

### Notebook 04 — ETL Unificado
Integra ventas Olist con la capa argentina, convierte BRL→ARS, ajusta por inflación y genera las dimensiones del modelo. Produce 7 archivos: `fact_ventas_final.csv` (110.197 filas), `fact_precios_comp.csv` (360), `dim_clientes_ar.csv` (10.000), `dim_inflacion_ipc.csv` (111), `dim_tiempo.csv` (3.288, 2016–2024), `dim_productos.csv` (32.951) y `dim_categorias.csv` (10). **Estado: Completo.**

### Notebook 05 — Market Basket Analysis
Descubre reglas de asociación (Apriori) a nivel categoría y producto sobre los 110.197 ítems vendidos, con soporte ≥ 0.01, confianza ≥ 0.30 y lift ≥ 1.20. Genera `market_basket_reglas.csv` y `market_basket_reglas_enriquecidas.csv` (con nombres CACE en español). **Estado: Completo.**

### Notebook 06 — Clustering de Clientes
Segmentación K-Means sobre features RFM (9.999 clientes en 4 clusters: Alto valor / Frecuente / Ocasional / Inactivo) y análisis de cohortes de retención mensual. Genera `clustering_clientes.csv`, `cohortes_retencion.csv`, `cohortes_resumen.csv` y `cohortes_matriz_ancha.csv`. **Estado: Completo.**

---

## 8. Modelo de Datos en Power BI

**Tipo de esquema:** Galaxia — 2 tablas de hechos, 8 dimensiones, 13 relaciones validadas, cardinalidad muchos-a-uno en todos los casos.

### Tablas de Hechos

| Tabla | Filas | Descripción |
|-------|-------|-------------|
| `FactVentasFinal` | 110.197 | Ventas Olist + contexto argentino sintético; granularidad = 1 ítem vendido en los tres canales |
| `FactPreciosComp` | 360 | Precios de competencia por categoría y mes (30 categorías × 12 meses) |

### Dimensiones Compartidas y de Apoyo

| Tabla | Rol |
|-------|-----|
| `DimTiempo` | **Date Table** — obligatoria para inteligencia de tiempo (TOTALYTD, SAMEPERIODLASTYEAR) |
| `DimProductos`, `DimCategorias`, `DimCanal` | Dimensiones compartidas entre ambas tablas de hechos, permiten análisis cruzados sin duplicar datos |
| `DimClientesAr`, `DimGeografia`, `DimSucursalesAr`, `DimInflacionIpc` | Dimensiones de apoyo del módulo de ventas |

`DimCanal → FactPreciosComp` es una relación **inactiva**, activada con `USERELATIONSHIP` solo cuando la medida lo requiere, para evitar ambigüedad de filtros.

### Tablas de Análisis Avanzado

`ClusteringClientes`, `CohortesRetencion`, `CohortesResumen`, `CohortesMatrizAncha` (notebook 06) y `MarketBasketReglas`, `MarketBasketEnriquecidas` (notebook 05).

### Tablas de Referencia CACE

11+ tablas `cace_*` cargadas como contexto de benchmark, sin relaciones formales en el modelo.

---

## 9. Estado de Avance

| Fase | Descripción | Estado |
|------|-------------|--------|
| 0 | Configuración del entorno | **Completo** |
| 1 | Generación de datos sintéticos argentinos | **Completo** |
| 2 | EDA Nivel 1 — diagnóstico individual | **Completo** |
| 3 | EDA Nivel 2 — validación de relaciones | **Completo** |
| 4 | ETL unificado (conversión + inflación + integración) | **Completo** |
| 5 | Market Basket Analysis (Apriori) | **Completo** |
| 6 | Clustering K-Means + cohortes de retención | **Completo** |
| 7 | Modelado de datos y dashboards en Power BI (10 páginas) | **Completo** |
| 8 | Análisis financiero: VAN, costos del proyecto | **Completo** |
| 9 | Defensa final del proyecto (06/07/2026) | **Completo** |

---

## 10. Resultados Clave (Dashboard Ejecutivo)

| Métrica | Valor |
|---------|-------|
| Ventas totales | $81,13 M |
| Órdenes únicas | ~96 mil |
| Ticket promedio | $840,93 |
| Margen bruto | $25,18 M |
| % Margen promedio | 31,03 % |

- 92 % de la facturación corresponde a canales digitales; el marketplace es el canal dominante.
- La brecha nominal vs. real (ajuste por inflación) se amplía notoriamente en 2018.
- Alimentos y Bebidas es la única categoría con price index > 1 (por encima del mercado).

### Viabilidad Económica (VAN)

| Año | Flujo |
|-----|-------|
| Año 0 | −USD 3.456 |
| Año 1 | +USD 3.444 |
| Año 2 | +USD 17.444 |
| Año 3 | +USD 38.224 |

VAN a 3 años (tasa de descuento 30 %): **USD 26.913, positivo**. Relación beneficio/costo ≈ 2,8:1. Punto de equilibrio: 3 clientes piloto a USD 150/mes cubren los gastos operativos del año 1.

---

## 11. Decisiones de Diseño Importantes

| Decisión | Justificación |
|----------|---------------|
| Usar solo órdenes "delivered" de Olist | Elimina órdenes canceladas o incompletas que distorsionarían métricas de ventas |
| Base de inflación = diciembre 2016 | Primer mes disponible en el dataset Olist; permite comparación real en toda la serie |
| SucursalID nulo en ~92 % de las filas | Comportamiento esperado: la mayoría de las ventas son online; no es un error de datos |
| PeriodoID = anio × 100 + mes | Permite join directo en Power BI sin columnas calculadas adicionales |
| DimCategorias como tabla puente | Resuelve relación N:N entre DimProductos y FactPreciosComp sin duplicar datos |
| Esquema galaxia, no estrella | Ventas y precios de competencia son procesos de negocio distintos, con granularidad propia, que igual necesitan compararse contra los mismos productos, períodos y canales |
| SEED=42 en generación sintética | Garantiza reproducibilidad total del dataset entre ejecuciones |
| Encoding UTF-8-SIG en los CSVs | Necesario para que Power BI y Excel interpreten correctamente caracteres acentuados del español |

---

## 12. Preguntas de Negocio que el Dashboard Responde

1. ¿Cuál es el ticket promedio por canal de venta?
2. ¿Cómo evolucionó el volumen de ventas en términos reales (ajustados por inflación)?
3. ¿Qué regiones concentran mayor facturación?
4. ¿Cuáles son las categorías de producto con mayor margen y volumen?
5. ¿Cómo se distribuyen los medios de pago y el financiamiento en cuotas?
6. ¿Cuánto tarda la logística por zona (AMBA vs. Interior)?
7. ¿Cómo se posiciona el precio propio vs. la competencia por categoría?
8. ¿Qué segmentos de clientes (RFM/K-Means) y qué productos se venden juntos (Market Basket) generan más oportunidad comercial?

---

## 13. Documentación Disponible en `extras/`

| Archivo | Contenido |
|---------|-----------|
| `00_configuracion_entorno_explicacion.md` | Guía narrativa del notebook 00 |
| `01_creador_datos_sinteticos_explicacion.md` | Guía narrativa del notebook 01 |
| `02_EDA_nivel_1_explicacion.md` | Guía narrativa del notebook 02 |
| `03_EDA_nivel_2_explicacion.md` | Guía narrativa del notebook 03 |
| `04_ETL_explicacion.md` | Explicación completa del pipeline ETL |
| `05_guia_tablas_power_bi.md` | Carga y configuración de tablas en Power BI (incluye tablas de notebooks 05 y 06) |
| `06_diagrama_relaciones.html` | Diagrama interactivo (canvas) del modelo completo de datos |
| `07_dashboard_validaciones_eda_etl.html` | Dashboard de validaciones y decisiones tomadas durante EDA/ETL |
| `08_dashboard_proyecto.html` | Dashboard explicativo integral del proyecto |
| `09_flujo_real_proyecto.html` | Diagrama de las 6 etapas reales de ejecución del proyecto |
| `10_matriz_riesgos_retailiq360.html` | Matriz de riesgos e impacto/probabilidad |
| `11_diagrama_de_pert_del_proyecto.html` | Diagrama PERT con ruta crítica (plan original) |
| `12_cronograma_interactivo_de_proyecto.html` | Cronograma Gantt planificado |
| `13_cronograma_gantt_plan_vs_realidad.html` | Comparativa plan vs. ejecución real |
| `14_ResumenProyecto_RetailIQ360.docx` | Resumen ejecutivo del proyecto |
| `15_procedimiento_actualizar_repositorio_github.md` | Guía paso a paso para hacer push a GitHub |
| `16_guia_github_paso_a_paso.md` | Guía complementaria de uso de GitHub |
| `diccionario_datos_RetailIQ360.xlsx` | Diccionario completo de tablas y columnas (generado por `notebooks/07_generar_diccionario.py`) |
| `VAN_RetailIQ360.xlsx` | Cálculo del Valor Actual Neto y estructura de costos |

También relevante: `docs/RetailIQ360_Presentacion_Defensa_06-07-2026.pptx` (presentación final de defensa).

---

## 14. Trabajo Futuro

1. Incorporar datos de costo real por SKU para un margen preciso.
2. Sumar datos de stock: sell-through rate y rotación de inventario.
3. Granularidad horaria para detectar patrones intradía (app móvil).
4. Dimensión de eventos comerciales (Hot Sale, CyberMonday).
5. Modelo predictivo de churn (regresión logística / Random Forest).

---

## 15. Instrucciones para el Agente de IA

### Cómo usar este contexto

- **Consultas de estado:** el proyecto está completo y defendido (sección 9); usar este contexto para explicar decisiones ya tomadas, no para planificar trabajo pendiente salvo lo listado en la sección 14.
- **Conflictos de datos:** verificar las Decisiones de Diseño (sección 11) antes de sugerir cambios; muchas decisiones tienen justificación técnica explícita.
- **Consultas de Power BI:** el modelo está documentado en la sección 8; para detalles de columnas, consultar `extras/diccionario_datos_RetailIQ360.xlsx`.
- **Preguntas sobre datos:** la sección 5 describe cada fuente y su rol; nunca mezclar la lógica de Olist (datos reales) con la de los sintéticos (datos generados).

### Criterios de evaluación del proyecto

El proyecto es exitoso si:
1. El pipeline de notebooks es reproducible de extremo a extremo ejecutándolos en orden (00→06).
2. Las tablas de `datos/04_procesados/` se cargan correctamente en Power BI sin errores de encoding ni de relaciones.
3. El modelo Power BI respeta las 13 relaciones documentadas en la sección 8.
4. El dashboard responde las 8 preguntas de negocio de la sección 12.
5. El VAN a 3 años es positivo bajo una tasa de descuento exigente (confirmado: sección 10).

### Limitaciones conocidas

- Los datos de ventas son históricos (2016–2018); no representan el mercado actual.
- Los clientes y sucursales son 100 % sintéticos; no existen en la realidad.
- El ajuste por inflación tiene un hueco de ~317 filas (sep–dic 2016) que debe tratarse en el dashboard.
- Power BI no procesa bien los archivos CSV sin BOM (UTF-8-SIG es obligatorio).
- El margen reportado usa un margen estimado por categoría, no costo real por SKU (ver trabajo futuro, punto 1).

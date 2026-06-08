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
| **Fecha de referencia** | Junio 2026 |

---

## 2. Objetivo General

Construir una plataforma integral de análisis que permita a una empresa de retail argentina visualizar KPIs clave, detectar patrones de compra y apoyar decisiones comerciales basadas en datos a través de cuatro canales de venta: **tienda física, web propia, app móvil y marketplace**.

---

## 3. Objetivos Específicos

1. Generar un conjunto de datos sintéticos representativos del mercado e-commerce argentino, calibrados con benchmarks reales (CACE 2025).
2. Aplicar un pipeline de ETL que unifique fuentes heterogéneas: datos transaccionales brasileños (Olist), contexto macroeconómico argentino (IPC INDEC, tipo de cambio BCRA) y datos sintéticos propios.
3. Construir un modelo de datos tipo galaxia en Power BI con tablas de hechos y dimensiones correctamente relacionadas.
4. Desarrollar un dashboard interactivo que responda preguntas de negocio omnicanal: ticket promedio, conversión, canales, geografía, inflación y competencia.

---

## 4. Stack Tecnológico

- **Lenguaje:** Python 3 con Jupyter (análisis, ETL, generación de datos)
- **Librerías principales:** Pandas ≥ 3.0, NumPy ≥ 2.0, Scikit-learn ≥ 1.8, Faker ≥ 24, Plotly ≥ 6.0, Seaborn, Matplotlib
- **BI:** Power BI Desktop (modelo + dashboard)
- **Control de versiones:** Git / GitHub
- **Entorno:** Windows 11, JupyterLab ≥ 4.0

---

## 5. Fuentes de Datos

| ID | Fuente | Descripción | Rol en el proyecto |
|----|--------|-------------|-------------------|
| **Olist** | Dataset público de e-commerce brasileño (2016–2018) | 110.197 transacciones reales con órdenes, ítems, productos y reseñas | Tabla de hechos principal (ventas) |
| **CACE 2025** | Cámara Argentina de Comercio Electrónico | 11 benchmarks: KPIs macro, categorías, medios de pago, logística, geografía | Calibración de datos sintéticos + tablas de referencia en Power BI |
| **IPC INDEC** | Índice de Precios al Consumidor (Argentina) | 111 meses de inflación mensual (2017–2026) | Deflactar precios a pesos constantes de dic-2016 |
| **Tipos de cambio BCRA** | Banco Central de la República Argentina | Cotizaciones diarias ARS/USD históricas | Convertir precios de BRL a ARS |
| **Datos sintéticos** | Generados con Faker (SEED=42) | Clientes, sucursales, canales, medios de pago, logística — contexto argentino | Enriquecer Olist con dimensiones omnicanal argentinas |

---

## 6. Estructura del Repositorio

```
integrador_carrera/
├── notebooks/              # Pipeline de análisis (5 notebooks numerados)
│   ├── 00_configuracion_entorno.ipynb
│   ├── 01_creador_datos_sinteticos.ipynb
│   ├── 02_EDA_nivel_1.ipynb
│   ├── 03_EDA_nivel_2.ipynb
│   └── 04_ETL.ipynb
├── datos/
│   ├── 01_raw/             # Datos originales sin modificar
│   ├── 02_cace_benchmarks/ # 11 archivos CSV de referencia CACE
│   ├── 03_sinteticos/      # Tablas generadas por notebook 01
│   └── 04_procesados/      # Salidas finales para Power BI (7 tablas)
├── power_bi/               # Archivo .pbix con el dashboard
├── extras/                 # Documentación narrativa y guías
├── docs/                   # Documentación final del proyecto
├── src/                    # Funciones helper reutilizables
├── diseño/                 # Diagramas del modelo de datos
└── requirements.txt        # Dependencias Python
```

---

## 7. Pipeline de Notebooks

### Notebook 00 — Configuración del Entorno
- Verifica versiones de librerías instaladas.
- Configura estilos visuales y formatos numéricos.
- Inventaría archivos de datos disponibles.
- **Estado: Completo.**

### Notebook 01 — Creador de Datos Sintéticos
Genera 6 tablas con SEED=42 para reproducibilidad:
- `001_dim_geografia_ar.csv` — 67 filas, jerarquía geográfica argentina calibrada con CACE.
- `002_dim_sucursales_ar.csv` — 50 sucursales (tienda grande, tienda chica, dark store).
- `003_dim_canal_ar.csv` — 4 canales con pesos CACE: físico 8%, web 25%, app 20%, marketplace 47%.
- `dim_clientes_ar.csv` — 10.000 clientes con NSE, rango etario, género, canal preferido.
- `fact_ventas_base_ar.csv` — 150.000 transacciones sintéticas (no es la tabla de hechos final).
- `006_fact_precios_comp.csv` — 360 precios de competencia por categoría/mes (2022–2024).
- **Estado: Completo.**

### Notebook 02 — EDA Nivel 1
- Diagnóstico individual de cada dataset: nulos, duplicados, tipos, estadísticas.
- Genera `dim_inflacion_ipc.csv` a partir del archivo INDEC.
- Decisión clave: usar solo órdenes Olist con estado "delivered".
- **Estado: Completo.**

### Notebook 03 — EDA Nivel 2
- Valida integridad referencial entre datasets (órdenes ↔ ítems ↔ productos).
- Verifica cobertura temporal IPC vs. fechas de ventas.
- Mapea 72 categorías Olist en inglés a 10 categorías CACE en español.
- Construye FactVentas preliminar para confirmar que el ETL es viable.
- **Estado: Completo.**

### Notebook 04 — ETL Unificado
Pipeline de 10 bloques sin dependencias intermedias:

| Bloque | Acción |
|--------|--------|
| 0 | Carga todos los inputs al inicio y valida disponibilidad |
| 1 | Genera base FactVentas: orders + items + productos (110.197 filas) |
| 2 | Convierte precios BRL → ARS (tipo de cambio = ARS/USD ÷ 3.3) con forward fill |
| 3 | Deflacta a pesos constantes dic-2016 usando IPC acumulado (317 filas sin cobertura) |
| 4 | Enriquece con canal, cliente, sucursal, medio de pago, cuotas, logística |
| 5 | Agrega GeografiaID a DimClientes |
| 6 | Agrega PeriodoID (AAAAMM) a DimInflacionIpc |
| 7 | Genera DimTiempo: 3.288 filas 2016–2024 con atributos en español |
| 8 | Genera DimProductos: 32.951 fichas con categoría CACE en español |
| 9 | Genera DimCategorias (10 filas) como tabla puente N:N |
| 10 | Guarda 7 archivos CSV con encoding UTF-8-SIG para Power BI |

**Estado: Completo.**

---

## 8. Modelo de Datos en Power BI

**Tipo de esquema:** Galaxia (dos tablas de hechos con dimensiones compartidas)

### Tablas de Hechos

| Tabla | Filas | Descripción |
|-------|-------|-------------|
| `fact_ventas_final.csv` | 110.197 | Ventas Olist + contexto argentino; granularidad = 1 ítem vendido |
| `fact_precios_comp.csv` | 360 | Precios de competencia por categoría y mes |

### Tablas de Dimensión (para carga en Power BI)

| Tabla | Filas | Rol |
|-------|-------|-----|
| `dim_tiempo.csv` | 3.288 | **Date Table** — obligatoria para inteligencia de tiempo (TOTALYTD, SAMEPERIODLASTYEAR) |
| `dim_clientes_ar.csv` | 10.000 | Perfil de clientes con GeografiaID |
| `dim_geografia_ar.csv` | 67 | Regiones, provincias, ciudades argentinas |
| `dim_sucursales_ar.csv` | 50 | Sucursales físicas |
| `dim_canal_ar.csv` | 4 | Canales de venta |
| `dim_productos.csv` | 32.951 | Productos con categoría CACE en español |
| `dim_categorias.csv` | 10 | Tabla puente — evita relación N:N entre productos y hechos |
| `dim_inflacion_ipc.csv` | 111 | Índice IPC mensual con acumulado base dic-2016 |

### Relaciones Clave

```
DimTiempo.Fecha          → FactVentasFinal.order_purchase_timestamp  (activa)
DimCanal.canal_id        → FactVentasFinal.canal_id
DimCanal.canal_id        → FactPreciosComp.canal_id
DimClientes.cliente_id   → FactVentasFinal.cliente_id
DimSucursales.id         → FactVentasFinal.sucursal_id
DimInflacion.PeriodoID   → FactVentasFinal.PeriodoID
DimProductos.product_id  → FactVentasFinal.product_id
DimCategorias.categoria  → DimProductos.categoria_es        (puente)
DimCategorias.categoria  → FactPreciosComp.categoria_es     (puente)
DimGeografia.GeografiaID → DimSucursales.GeografiaID
DimGeografia.GeografiaID → DimClientes.GeografiaID
```

### Tablas de Referencia CACE (sin relaciones formales)
11 tablas `cace_XX_*.csv` cargadas en Power BI como contexto de benchmark.

---

## 9. Estado de Avance

| Fase | Descripción | Estado |
|------|-------------|--------|
| 0 | Configuración del entorno | **Completo** |
| 1 | Generación de datos sintéticos argentinos | **Completo** |
| 2 | EDA Nivel 1 — diagnóstico individual | **Completo** |
| 3 | EDA Nivel 2 — validación de relaciones | **Completo** |
| 4 | ETL unificado (conversión + inflación + integración) | **Completo** |
| 5 | Modelado de datos en Power BI | **En progreso** |
| 6 | Dashboard interactivo y presentación final | **En progreso** |

---

## 10. Decisiones de Diseño Importantes

| Decisión | Justificación |
|----------|---------------|
| Usar solo órdenes "delivered" de Olist | Elimina órdenes canceladas o incompletas que distorsionarían métricas de ventas |
| Base de inflación = diciembre 2016 | Primer mes disponible en el dataset Olist; permite comparación real en toda la serie |
| SucursalID nulo en ~92% de las filas | Comportamiento esperado: la mayoría de las ventas son online; no es un error de datos |
| PeriodoID = anio × 100 + mes | Permite join directo en Power BI sin columnas calculadas adicionales |
| DimCategorias como tabla puente | Resuelve relación N:N entre DimProductos y FactPreciosComp sin duplicar datos |
| DimTiempo marcada como Date Table | Obligatorio en Power BI para que funcionen las funciones de inteligencia de tiempo (TOTALYTD, SAMEPERIODLASTYEAR, etc.) |
| SEED=42 en generación sintética | Garantiza reproducibilidad total del dataset entre ejecuciones |
| Encoding UTF-8-SIG en los CSVs | Necesario para que Power BI y Excel interpreten correctamente caracteres acentuados del español |
| ~317 filas sin cobertura IPC | Sep–dic 2016 están fuera del rango del IPC disponible; tienen_ipc=False y pueden filtrarse en el dashboard |

---

## 11. Preguntas de Negocio que el Dashboard Debe Responder

1. ¿Cuál es el ticket promedio por canal de venta?
2. ¿Cómo evolucionó el volumen de ventas en términos reales (ajustados por inflación)?
3. ¿Qué regiones concentran mayor facturación?
4. ¿Cuáles son las categorías de producto con mayor margen y volumen?
5. ¿Cómo se distribuyen los medios de pago y el financiamiento en cuotas?
6. ¿Cuánto tarda la logística por zona (AMBA vs. Interior)?
7. ¿Cómo se posiciona el precio propio vs. la competencia por categoría?
8. ¿Qué impacto tienen los eventos comerciales (Hot Sale, CyberMonday) en las ventas?

---

## 12. Documentación Disponible

| Archivo | Ubicación | Contenido |
|---------|-----------|-----------|
| `README.md` | raíz | Descripción general del proyecto |
| `00_configuracion_entorno_explicacion.md` | `extras/` | Guía narrativa del notebook 00 |
| `01_creador_datos_sinteticos_explicacion.md` | `extras/` | Guía narrativa del notebook 01 |
| `02_EDA_nivel_1_explicacion.md` | `extras/` | Guía narrativa del notebook 02 |
| `03_EDA_nivel_2_explicacion.md` | `extras/` | Guía narrativa del notebook 03 |
| `04_ETL_explicacion.md` | `extras/` | Explicación completa del pipeline ETL |
| `05_guia_tablas_power_bi.md` | `extras/` | Carga y configuración de tablas en Power BI |
| `diccionario_datos_RetailIQ360.xlsx` | `extras/` | Diccionario completo de tablas y columnas |
| `06_diagrama_relaciones.html` | `extras/` | Diagrama interactivo del modelo |
| `07_modelo_relaciones_estrella_galaxia.svg` | `extras/` | Diagrama SVG del esquema de datos |

---

## 13. Instrucciones para el Agente de IA

### Cómo usar este contexto

- **Consultas de estado:** referirse a la sección 9 (Estado de Avance) y a los archivos de los notebooks para determinar qué está hecho y qué no.
- **Conflictos de datos:** verificar las Decisiones de Diseño (sección 10) antes de sugerir cambios; muchas decisiones tienen justificación técnica explícita.
- **Consultas de Power BI:** el modelo está documentado en la sección 8; para detalles de columnas, consultar `extras/diccionario_datos_RetailIQ360.xlsx`.
- **Preguntas sobre datos:** la sección 5 describe cada fuente y su rol; nunca mezclar la lógica de Olist (datos reales) con la de los sintéticos (datos generados).
- **Evaluación de avance:** las fases 0–4 están completas; las fases 5 y 6 (Power BI y dashboard) están en progreso y son el foco actual.

### Criterios de evaluación del proyecto

El proyecto es exitoso si:
1. El pipeline ETL es reproducible de extremo a extremo ejecutando los notebooks en orden (00→04).
2. Las 7 tablas de `datos/04_procesados/` se cargan correctamente en Power BI sin errores de encoding ni de relaciones.
3. El modelo Power BI respeta las relaciones documentadas en la sección 8.
4. El dashboard responde las 8 preguntas de negocio de la sección 11.
5. Los datos sintéticos son coherentes con los benchmarks CACE 2025.

### Limitaciones conocidas

- Los datos de ventas son históricos (2016–2018); no representan el mercado actual.
- Los clientes y sucursales son 100% sintéticos; no existen en la realidad.
- El ajuste por inflación tiene un hueco de 317 filas (sep–dic 2016) que debe tratarse en el dashboard.
- Power BI no procesa bien los archivos CSV sin BOM (UTF-8-SIG es obligatorio).

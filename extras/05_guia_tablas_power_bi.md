# Guía de tablas para Power BI — RetailIQ360

Descripción de cada tabla, sus relaciones y las verificaciones principales a realizar antes de construir el modelo.

---

## Índice

1. [Dimensiones](#1-dimensiones)
2. [Tablas de hechos](#2-tablas-de-hechos)
3. [Analítica derivada](#3-analitica-derivada)
4. [Benchmarks CACE](#4-benchmarks-cace)
5. [Orden de carga y relaciones](#5-orden-de-carga-y-relaciones)
6. [Verificaciones generales](#6-verificaciones-generales)

> **Última actualización:** modelo ampliado a esquema galaxia, esquema SQL v2 disponible en `sql/retailiq360_schema.sql` y nueva etapa `05_market_basket.ipynb`. Se agregaron las salidas `market_basket_reglas.csv`, `market_basket_reglas_enriquecidas.csv`, `market_basket_heatmap.png` y `market_basket_top10.png` en `datos/04_procesados/`. Ver sección 5 para el orden de carga y relaciones actualizados.

---

## 1. Dimensiones

### dim_geografia_ar
**Carpeta:** `03_sinteticos/001_dim_geografia_ar.csv`  
**Filas:** 67 | **Columnas:** 6

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `GeografiaID` | Entero | Clave primaria |
| `region` | Texto | Región macro: AMBA, Centro, NOA, etc. |
| `provincia` | Texto | Nombre completo de la provincia |
| `ciudad` | Texto | Ciudad o localidad |
| `zona` | Texto | AMBA o Interior |
| `peso_facturacion` | Decimal | Peso relativo de facturación calibrado con CACE |

**Relaciones:**
- `GeografiaID` → referenciada por `dim_sucursales_ar.GeografiaID` (1:N)
- `GeografiaID` → referenciada por `dim_clientes_ar.GeografiaID` (1:N)
- `region` → comparable con `cace_06a_distribucion_regional.region`

**Verificaciones:**
- [ ] No hay `GeografiaID` duplicados
- [ ] Los 67 registros cubren todas las provincias de Argentina
- [ ] `peso_facturacion` suma 1.0 agrupado por zona o región
- [ ] Ningún valor nulo en `GeografiaID`, `region`, `provincia`, `ciudad`

---

### dim_canal_ar
**Carpeta:** `03_sinteticos/003_dim_canal_ar.csv`  
**Filas:** 4 | **Columnas:** 6

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `CanalID` | Entero | Clave primaria (1 a 4) |
| `nombre` | Texto | Nombre del canal: Tienda física, Web propia, App móvil, Marketplace |
| `tipo` | Texto | Físico, Online o Marketplace |
| `plataforma` | Texto | POS físico, Sitio web, App iOS/Android, MercadoLibre |
| `flag_online` | Entero | 0 = presencial, 1 = online |
| `peso_facturacion` | Decimal | Peso calibrado con CACE: Físico 8%, Web 25%, App 20%, Marketplace 47% |

**Relaciones:**
- `CanalID` → referenciada por `fact_ventas_final.CanalID` (1:N)
- `CanalID` → referenciada por `fact_precios_comp.CanalID` (1:N)
- `nombre` → comparable con `cace_07_canal_online_por_categoria`

**Verificaciones:**
- [ ] Exactamente 4 filas, sin duplicados
- [ ] `peso_facturacion` suma exactamente 1.0
- [ ] `flag_online` contiene solo valores 0 y 1
- [ ] Los 4 `CanalID` (1, 2, 3, 4) están presentes en `fact_ventas_final`

---

### dim_sucursales_ar
**Carpeta:** `03_sinteticos/002_dim_sucursales_ar.csv`  
**Filas:** 50 | **Columnas:** 11

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `SucursalID` | Entero | Clave primaria |
| `nombre` | Texto | Nombre de la sucursal (ej: "RetailIQ Avellaneda 1") |
| `tipo` | Texto | Tienda grande, Tienda chica, Dark store |
| `GeografiaID` | Entero | FK → `dim_geografia_ar` |
| `provincia` | Texto | Provincia donde está la sucursal |
| `ciudad` | Texto | Ciudad donde está la sucursal |
| `region` | Texto | Región macro |
| `m2_ventas` | Entero | Metros cuadrados del área de ventas |
| `empleados` | Entero | Cantidad de empleados |
| `fecha_apertura` | Fecha | Fecha de apertura de la sucursal |
| `flag_activa` | Entero | 1 = activa, 0 = cerrada |

**Relaciones:**
- `GeografiaID` → `dim_geografia_ar.GeografiaID` (N:1)
- `SucursalID` → referenciada por `fact_ventas_final.SucursalID` (1:N)

> **Importante:** `SucursalID` tiene nulos en `fact_ventas_final` para todas las ventas de canales digitales (CanalID 2, 3 y 4). Esto es esperado y representa el 92% de las filas. Power BI tolera la FK nula en el lado N de la relación.

**Verificaciones:**
- [ ] No hay `SucursalID` duplicados
- [ ] Todos los `GeografiaID` existen en `dim_geografia_ar`
- [ ] `flag_activa` contiene solo valores 0 y 1
- [ ] `fecha_apertura` tiene formato fecha válido (sin texto ni nulos)
- [ ] `m2_ventas` y `empleados` son valores positivos

---

### dim_clientes_ar
**Carpeta:** `04_procesados/dim_clientes_ar.csv`  
**Filas:** 10.000 | **Columnas:** 15

> Esta tabla fue generada en `01_creador_datos_sinteticos.ipynb` y luego procesada por el bloque 5 de `04_ETL.ipynb`, que incorporó la columna `GeografiaID` mediante un join cascado con `dim_geografia_ar`. El archivo resultante se guardó en `04_procesados/` (ya no en `03_sinteticos/`).

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `ClienteID` | Entero | Clave primaria |
| `GeografiaID` | Entero | FK → `dim_geografia_ar` (incorporado por el ETL) |
| `nombre` | Texto | Nombre completo (generado con Faker) |
| `email` | Texto | Email del cliente |
| `telefono` | Texto | Teléfono con formato argentino (+54) |
| `provincia` | Texto | Provincia de residencia |
| `ciudad` | Texto | Ciudad de residencia |
| `region` | Texto | Región macro |
| `zona` | Texto | AMBA o Interior |
| `nse` | Texto | Nivel socioeconómico: ABC1, C2, C3, D (calibrado CACE) |
| `rango_edad` | Texto | Segmento etario: 18-20, 21-29, 30-34, 35-44, 45-59, 60+ |
| `genero` | Texto | M o F (50/50 calibrado CACE) |
| `canal_preferido` | Texto | Canal de compra preferido |
| `segmento_rfm` | Texto | Segmento RFM — columna vacía, se puede eliminar en Power Query |
| `fecha_alta` | Fecha | Fecha de registro del cliente |

**Relaciones:**
- `ClienteID` → referenciada por `fact_ventas_final.ClienteID` (1:N)
- `GeografiaID` → `dim_geografia_ar.GeografiaID` (N:1)

> **Cambio respecto a la versión anterior:** `dim_clientes_ar` ahora tiene una columna `GeografiaID` que actúa como clave foránea formal hacia `dim_geografia_ar`. Esto permite construir el mapa de calor por provincia directamente desde la tabla de clientes y relacionarla con la jerarquía geográfica en Power BI.

**Verificaciones:**
- [ ] No hay `ClienteID` duplicados (deben ser 10.000 únicos)
- [ ] Todos los `ClienteID` de `fact_ventas_final` existen en esta tabla
- [ ] `GeografiaID` no tiene nulos (el ETL usó fallback por provincia)
- [ ] Distribución de `nse`: ABC1 ~24%, C2 ~26%, C3 ~30%, D ~20%
- [ ] Distribución de `genero`: ~50% M y ~50% F
- [ ] `email` sin duplicados
- [ ] `fecha_alta` tiene formato fecha válido
- [ ] Eliminar `segmento_rfm` en Power Query (100% nulo)

---

### dim_inflacion_ipc
**Carpeta:** `04_procesados/dim_inflacion_ipc.csv`  
**Filas:** 111 | **Columnas:** 11

> Esta tabla fue procesada por el bloque 6 de `04_ETL.ipynb`, que incorporó `PeriodoID` (clave de relación numérica) e `indice_ipc_acum` (índice acumulado calculado en el pipeline). Estas dos columnas la hacen autocontenida y permiten relacionarla directamente con `fact_ventas_final` sin necesidad de columnas calculadas en Power BI.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `PeriodoID` | Entero | Clave primaria compuesta: `anio × 100 + mes` (ej: octubre 2017 → 201710) |
| `fecha` | Fecha | Primer día del mes (ej: 2017-01-01) |
| `ipc_nivel_general` | Decimal | Variación mensual IPC general en % |
| `ipc_alimentos_bebidas` | Decimal | Variación mensual IPC alimentos y bebidas |
| `ipc_indumentaria_calzado` | Decimal | Variación mensual IPC indumentaria |
| `ipc_equipamiento_hogar` | Decimal | Variación mensual IPC equipamiento hogar |
| `ipc_transporte` | Decimal | Variación mensual IPC transporte |
| `ipc_comunicacion` | Decimal | Variación mensual IPC comunicación |
| `anio` | Entero | Año (2017 a 2026) |
| `mes` | Entero | Mes (1 a 12) |
| `indice_ipc_acum` | Decimal | Índice acumulado desde diciembre 2016 (base = 1.0) |

**Relaciones:**
- `PeriodoID` → referenciada por `fact_ventas_final.PeriodoID` (1:N)
- `ipc_nivel_general` → comparable con `cace_01_kpis_macro` (inflación interanual)

> **Cambio respecto a la versión anterior:** la relación ya no requiere una columna calculada `anio_mes` en Power BI. `PeriodoID` es una clave numérica directa disponible en ambas tablas. Seleccionar `dim_inflacion_ipc.PeriodoID → fact_ventas_final.PeriodoID` en Model View.

**Verificaciones:**
- [ ] No hay `PeriodoID` duplicados
- [ ] La serie es continua (sin huecos de meses)
- [ ] Ningún valor nulo en `ipc_nivel_general`
- [ ] `indice_ipc_acum` empieza en 1.0 (diciembre 2016) y es siempre creciente
- [ ] Los valores de `ipc_nivel_general` son razonables (entre -5% y 30% mensual)

---

### dim_tiempo
**Carpeta:** `04_procesados/dim_tiempo.csv`  
**Filas:** 3.288 | **Columnas:** 14

> Tabla de fechas completa generada por el bloque 7 de `04_ETL.ipynb`. Cubre el rango 2016-01-01 a 2024-12-31 (años completos) para cubrir tanto `fact_ventas_final` (2016–2018) como `fact_precios_comp` (2022–2024). **Debe marcarse como "Tabla de fechas" en Power BI** (Herramientas de tabla → Marcar como tabla de fechas → columna `fecha`). Sin este paso, TOTALYTD, SAMEPERIODLASTYEAR y otras medidas de inteligencia de tiempo no funcionan.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `TiempoID` | Entero | Clave primaria: `YYYYMMDD` (ej: 20171015) |
| `fecha` | Fecha | Fecha del día — columna del Date Table |
| `anio` | Entero | Año (2016, 2017, 2018) |
| `semestre` | Entero | 1 o 2 |
| `trimestre` | Entero | 1 a 4 |
| `mes` | Entero | Mes (1 a 12) |
| `nombre_mes` | Texto | Nombre en español: Enero, Febrero, ... Diciembre |
| `dia` | Entero | Día del mes (1 a 31) |
| `dia_semana` | Entero | 0 = lunes, 6 = domingo |
| `nombre_dia` | Texto | Nombre en español: Lunes, Martes, ... Domingo |
| `semana_anio` | Entero | Semana del año (ISO) |
| `es_fin_semana` | Booleano | True para sábado y domingo |
| `anio_mes` | Texto | Formato YYYY-MM (ej: "2017-10") — para etiquetas de eje |
| `PeriodoID` | Entero | `anio × 100 + mes` — consistente con `dim_inflacion_ipc.PeriodoID` |

**Relaciones:**
- `fecha` → referenciada por `fact_ventas_final.fecha` (1:N) — **relación principal del Date Table**
- `fecha` → referenciada por `fact_precios_comp.fecha_relevamiento` (1:N)

> **Configuración en Power BI:**  
> 1. Cargar `dim_tiempo.csv`.  
> 2. En Model View, seleccionar la tabla y abrir Herramientas de tabla → Marcar como tabla de fechas → elegir columna `fecha`.  
> 3. Establecer la relación `dim_tiempo.fecha → fact_ventas_final.fecha`.  
> 4. Establecer la relación `dim_tiempo.fecha → fact_precios_comp.fecha_relevamiento` (columnas con distinto nombre — crear manualmente).  
> 5. Verificar que `fecha` no tenga valores nulos y que cubra el rango completo de ambas tablas de hechos.

**Verificaciones:**
- [ ] 3.288 filas exactas (2016-01-01 a 2024-12-31, con años bisiestos 2016, 2020, 2024)
- [ ] `fecha` sin duplicados y sin nulos
- [ ] La columna `fecha` cubre desde 2016-01-01 hasta 2024-12-31
- [ ] `nombre_mes` en español (Enero, Febrero... no January)
- [ ] `es_fin_semana` es True solo para sábados y domingos (~28% de las filas)
- [ ] Todos los valores de `fact_ventas_final.fecha` tienen correspondencia en `dim_tiempo.fecha`
- [ ] Todos los valores de `fact_precios_comp.fecha_relevamiento` (día 15 de cada mes, 2022–2024) tienen correspondencia en `dim_tiempo.fecha`

---

### dim_productos
**Carpeta:** `04_procesados/dim_productos.csv`  
**Filas:** 32.951 | **Columnas:** 9

> Generada por el bloque 8 de `04_ETL.ipynb` a partir de las fichas de producto originales de Olist. Incluye `categoria_es` (clasificación CACE en español) que permite relacionar esta tabla con `dim_categorias` y, a través de ella, con `fact_precios_comp`.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `product_id` | Texto | Clave primaria (ID original de Olist) |
| `product_category_name` | Texto | Categoría en portugués (original Olist) |
| `category_en` | Texto | Categoría en inglés (72 categorías Olist) |
| `categoria_es` | Texto | Categoría CACE en español (10 categorías) — FK → `dim_categorias` |
| `product_weight_g` | Decimal | Peso del producto en gramos |
| `product_length_cm` | Decimal | Longitud en centímetros |
| `product_height_cm` | Decimal | Altura en centímetros |
| `product_width_cm` | Decimal | Ancho en centímetros |
| `volumen_cm3` | Decimal | Volumen calculado (largo × alto × ancho) |

**Relaciones:**
- `product_id` → referenciada por `fact_ventas_final.product_id` (1:N)
- `categoria_es` → `dim_categorias.categoria_es` (N:1)

> **Nota:** las 2 filas con nulos en dimensiones físicas fueron imputadas con la mediana de cada columna. Los 610 productos sin categoría asignada en Olist usan `other` → mapeado a `Hogar y Deco` en `categoria_es`.

**Verificaciones:**
- [ ] 32.951 filas exactas, sin `product_id` duplicados
- [ ] `categoria_es` tiene exactamente 10 valores distintos (las 10 categorías CACE)
- [ ] `product_weight_g`, `product_length_cm`, `product_height_cm`, `product_width_cm` sin nulos
- [ ] `volumen_cm3` = `product_length_cm × product_height_cm × product_width_cm` (verificar con medida DAX)
- [ ] Todos los `product_id` de `fact_ventas_final` existen en esta tabla

---

### dim_categorias
**Carpeta:** `04_procesados/dim_categorias.csv`  
**Filas:** 10 | **Columnas:** 2

> Tabla puente generada por el bloque 9 de `04_ETL.ipynb`. Contiene una fila por categoría CACE, permitiendo dos relaciones 1:N limpias en lugar de una relación N:N directa entre `dim_productos` y `fact_precios_comp`.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `CategoriaID` | Entero | Clave primaria (1 a 10) |
| `categoria_es` | Texto | Nombre de la categoría CACE en español |

**Categorías disponibles:** Accesorios Vehículos, Alimentos y Bebidas, Belleza, Construcción, Deportes, Electrodomésticos, Electrónica, Hogar y Deco, Indumentaria, Infantil.

**Relaciones:**
- `categoria_es` → referenciada por `dim_productos.categoria_es` (1:N)
- `categoria_es` → referenciada por `fact_precios_comp.categoria` (1:N) — columnas con distinto nombre, crear manualmente

> **Por qué existe esta tabla:** `dim_productos` tiene miles de productos por categoría y `fact_precios_comp` tiene decenas de filas por categoría. Una relación directa entre ambas sería N:N. `dim_categorias` actúa como puente con valores únicos en `categoria_es`, haciendo que ambas relaciones sean 1:N.

**Verificaciones:**
- [ ] Exactamente 10 filas, sin duplicados en `categoria_es`
- [ ] Los 10 valores de `categoria_es` coinciden exactamente con los de `dim_productos.categoria_es`
- [ ] Los 10 valores de `categoria_es` coinciden exactamente con los de `fact_precios_comp.categoria`

---

## 2. Tablas de hechos

### fact_ventas_final
**Carpeta:** `04_procesados/fact_ventas_final.csv`  
**Filas:** 110.197 | **Columnas:** 28

Esta es la **tabla central del modelo**. Fue construida en `04_ETL.ipynb` como pipeline unificado: toma transacciones reales de Olist Brasil (2016-2018), las convierte a ARS con el tipo de cambio BCRA, las deflacta con el IPC del INDEC y les asigna el contexto del mercado e-commerce argentino calibrado con benchmarks CACE 2025.

| Grupo | Columna | Tipo | Descripción |
|-------|---------|------|-------------|
| **Claves** | `VentaID` | Entero | Clave primaria (secuencial) |
| | `ClienteID` | Entero | FK → `dim_clientes_ar` |
| | `CanalID` | Entero | FK → `dim_canal_ar` (1=Físico, 2=Web, 3=App, 4=Marketplace) |
| | `SucursalID` | Entero | FK → `dim_sucursales_ar` (nulo si canal digital) |
| | `PeriodoID` | Entero | FK → `dim_inflacion_ipc` (`anio × 100 + mes`) |
| **Temporal** | `fecha` | Fecha | FK → `dim_tiempo.fecha` (Date Table) |
| | `anio` | Entero | Año (2016 a 2018) |
| | `mes` | Entero | Mes (1 a 12) |
| | `trimestre` | Entero | Trimestre (1 a 4) |
| **Producto** | `category_en` | Texto | Categoría del producto en inglés (72 categorías Olist) |
| **Contexto AR** | `medio_pago` | Texto | Medio de pago (calibrado CACE 04a MID 2023) |
| | `nro_cuotas` | Entero | Número de cuotas: 1, 3, 6, 10, 15 (calibrado CACE 04b 2025) |
| | `tipo_entrega` | Texto | Tipo de entrega (calibrado CACE 05a 2025) |
| | `plazo_entrega` | Texto | Plazo de entrega (calibrado CACE 05b 2024) |
| | `cantidad` | Entero | Unidades vendidas |
| **Precios BRL** | `precio_venta_brl` | Decimal | Precio original en Reales brasileños |
| | `flete_brl` | Decimal | Flete original en Reales brasileños |
| **Tipo de cambio** | `ars_por_usd` | Decimal | Tipo de cambio ARS/USD del BCRA (forward fill en feriados) |
| | `tipo_cambio` | Decimal | Factor de conversión BRL→ARS (`ars_por_usd ÷ 3.3`) |
| **Precios ARS nominal** | `precio_venta_ars` | Decimal | Precio en ARS al tipo de cambio del día |
| | `flete_ars` | Decimal | Flete en ARS al tipo de cambio del día |
| **Inflación** | `ipc_nivel_general` | Decimal | Variación IPC del mes (del INDEC) |
| | `indice_ipc_acum` | Decimal | Índice acumulado desde diciembre 2016 (base = 1.0) |
| | `precio_venta_ars_real` | Decimal | Precio en ARS constantes deflactado a diciembre 2016 |
| | `tiene_ipc` | Booleano | True si tiene cobertura IPC; False para sep–dic 2016 (~317 filas) |
| **Trazabilidad** | `order_id` | Texto | ID de la orden original de Olist |
| | `product_id` | Texto | ID del producto original de Olist |
| | `seller_id` | Texto | ID del vendedor original de Olist |

**Relaciones:**
- `ClienteID` → `dim_clientes_ar.ClienteID` (N:1)
- `CanalID` → `dim_canal_ar.CanalID` (N:1)
- `SucursalID` → `dim_sucursales_ar.SucursalID` (N:1, admite nulos)
- `fecha` → `dim_tiempo.fecha` (N:1) — relación principal del Date Table
- `PeriodoID` → `dim_inflacion_ipc.PeriodoID` (N:1)
- `product_id` → `dim_productos.product_id` (N:1)

> **Nota sobre SucursalID:** 101.468 filas (~92%) tienen `SucursalID` nulo porque corresponden a ventas de canales digitales (CanalID 2, 3 y 4). Esto es correcto y esperado. No filtrar estos nulos al construir el modelo.

> **Nota sobre tiene_ipc:** las ~317 filas con `tiene_ipc = False` son ventas de sep–dic 2016, período sin datos del INDEC. En esas filas `indice_ipc_acum = 1.0` y `precio_venta_ars_real = precio_venta_ars`. Se puede usar esta columna como filtro en el dashboard para excluirlas de análisis de inflación.

**Verificaciones:**
- [ ] 110.197 filas exactas después de la carga
- [ ] `VentaID` sin duplicados
- [ ] `fecha` entre 2016-09-02 y 2018-08-29
- [ ] `precio_venta_brl` y `precio_venta_ars` son valores positivos (sin ceros ni negativos)
- [ ] `SucursalID` nulo solo cuando `CanalID` es 2, 3 o 4
- [ ] `tiene_ipc` es False solo para fechas entre sep 2016 y dic 2016
- [ ] `indice_ipc_acum` empieza en 1.0 y crece con el tiempo
- [ ] `precio_venta_ars_real = precio_venta_ars / indice_ipc_acum` (verificar con medida DAX)
- [ ] `PeriodoID` = `anio * 100 + mes` (ej: octubre 2017 = 201710)

---

### fact_precios_comp
**Carpeta:** `04_procesados/fact_precios_comp.csv`  
**Filas:** 360 | **Columnas:** 12

> Procesada por el bloque 9 de `04_ETL.ipynb` a partir de `03_sinteticos/006_fact_precios_comp.csv`. Se le agregó `PeriodoID` para relacionarla con `dim_inflacion_ipc`. Cubre 2022–2024 (10 categorías × 12 meses × 3 años).

Precios relevados por categoría y mes, incluyendo precio propio y precio de competencia. Tabla de hechos secundaria para análisis de posicionamiento de precios frente al mercado.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `PrecioID` | Entero | Clave primaria |
| `categoria` | Texto | Categoría CACE en español — FK → `dim_categorias.categoria_es` |
| `anio` | Entero | Año del relevamiento |
| `mes` | Entero | Mes del relevamiento |
| `fecha_relevamiento` | Fecha | Día 15 de cada mes — FK → `dim_tiempo.fecha` |
| `precio_lista_ars` | Decimal | Precio de lista propio en ARS |
| `precio_web_ars` | Decimal | Precio online propio en ARS |
| `precio_competencia` | Decimal | Precio promedio de competencia en ARS |
| `descuento_pct` | Decimal | Descuento aplicado (entre 0 y 1) |
| `price_index` | Decimal | Índice precio propio / precio competencia (< 1 = más barato) |
| `CanalID` | Entero | FK → `dim_canal_ar` |
| `PeriodoID` | Entero | FK → `dim_inflacion_ipc` (`anio × 100 + mes`) — agregado por el ETL |

**Relaciones:**
- `fecha_relevamiento` → `dim_tiempo.fecha` (N:1) — columnas con distinto nombre, crear manualmente
- `PeriodoID` → `dim_inflacion_ipc.PeriodoID` (N:1)
- `CanalID` → `dim_canal_ar.CanalID` (N:1)
- `categoria` → `dim_categorias.categoria_es` (N:1) — columnas con distinto nombre, crear manualmente

**Verificaciones:**
- [ ] 360 filas exactas (10 categorías × 12 meses × 3 años)
- [ ] No hay `PrecioID` duplicados
- [ ] `PeriodoID` cubre de 202201 a 202412
- [ ] Todos los `CanalID` existen en `dim_canal_ar`
- [ ] Los 10 valores de `categoria` coinciden exactamente con `dim_categorias.categoria_es`
- [ ] `fecha_relevamiento` es siempre el día 15 del mes y existe en `dim_tiempo.fecha`
- [ ] `descuento_pct` está entre 0 y 1
- [ ] `price_index` es positivo
- [ ] `precio_web_ars` < `precio_lista_ars` en la mayoría de los casos

---

## 3. Analítica derivada

Estas tablas no forman parte del modelo relacional principal. Se generan a partir de `notebooks/05_market_basket.ipynb` y se cargan como apoyo visual para explicar patrones de compra conjunta, venta cruzada y recomendaciones.

---

### market_basket_reglas
**Carpeta:** `04_procesados/market_basket_reglas.csv`
**Filas:** 4 | **Columnas:** 9

Reglas de asociación exportadas por el notebook 05 usando Apriori y `mlxtend`. Actualmente las reglas se calculan sobre órdenes multi-ítem y combinan nivel categoría/producto según los resultados disponibles.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `nivel` | Texto | Granularidad de la regla: categoría o producto |
| `antecedentes` | Texto | Elemento o conjunto de partida de la regla |
| `consecuentes` | Texto | Elemento o conjunto recomendado cuando aparece el antecedente |
| `support` | Decimal | Proporción de órdenes donde aparece la combinación |
| `confidence` | Decimal | Probabilidad condicional de comprar el consecuente dado el antecedente |
| `lift` | Decimal | Fuerza de asociación frente al azar; > 1 indica asociación positiva |
| `leverage` | Decimal | Diferencia entre frecuencia observada y esperada bajo independencia |
| `conviction` | Decimal | Métrica de dependencia direccional de la regla |
| `zhangs_metric` | Decimal | Métrica adicional de asociación generada por `mlxtend` |

**Relaciones:**
- No crear relaciones formales. Es una tabla analítica derivada para visualizaciones de reglas.

**Verificaciones:**
- [ ] 4 filas actuales después de ejecutar `05_market_basket.ipynb`
- [ ] `support`, `confidence`, `lift`, `leverage` y `conviction` son numéricas
- [ ] `lift` > 1 para las reglas significativas
- [ ] La tabla se actualiza si cambian los parámetros `MIN_SUPPORT`, `MIN_CONFIANZA`, `MIN_LIFT` o el subconjunto analizado

---

### market_basket_reglas_enriquecidas
**Carpeta:** `04_procesados/market_basket_reglas_enriquecidas.csv`
**Filas:** 4 | **Columnas:** 11

Versión legible de las reglas de asociación, preparada para etiquetas de dashboard y explicaciones ejecutivas.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `regla` | Texto | Etiqueta corta de la regla |
| `regla_detalle` | Texto | Explicación legible para el dashboard |
| `categoria_antecedente` | Texto | Categoría CACE del antecedente |
| `categoria_consecuente` | Texto | Categoría CACE del consecuente |
| `antecedentes` | Texto | Antecedente original exportado por el notebook |
| `consecuentes` | Texto | Consecuente original exportado por el notebook |
| `support` | Decimal | Soporte de la regla |
| `confidence` | Decimal | Confianza de la regla |
| `lift` | Decimal | Lift de la regla |
| `leverage` | Decimal | Leverage de la regla |
| `conviction` | Decimal | Conviction de la regla |

**Relaciones:**
- No crear relaciones formales. Usar como tabla de etiquetas y narrativa para visuales de Market Basket.

**Archivos visuales generados por el notebook 05:**
- `market_basket_heatmap.png`: heatmap de lift entre categorías.
- `market_basket_top10.png`: gráfico de reglas principales por lift.

---

## 4. Benchmarks CACE

Las tablas CACE son **tablas de referencia**, no se conectan mediante relaciones formales en el modelo. Se usan directamente en visualizaciones para trazar líneas de benchmark.

---

### cace_01_kpis_macro
**Carpeta:** `02_cace_benchmarks/cace_01_kpis_macro.csv`  
**Filas:** 50 | **Columnas:** 7

Indicadores macroeconómicos del eCommerce argentino (2021-2025): facturación total, órdenes, unidades vendidas, ticket promedio, tasa de conversión, inflación, crecimiento YoY.

**Columnas clave:** `indicador`, `anio`, `periodo` (Anual / H1 / MID), `valor`, `unidad`

**Uso en Power BI:** Tarjetas de KPI con valor de referencia del mercado. Comparar ticket promedio propio vs. `ticket promedio` del sector.

**Verificaciones:**
- [ ] No hay combinaciones `(indicador, anio, periodo)` duplicadas
- [ ] `valor` no tiene nulos en los indicadores principales
- [ ] Columna `uso_proyecto` distingue benchmark, kpi_referencia, contexto y sintetico

---

### cace_02_categorias_rubros
**Carpeta:** `02_cace_benchmarks/cace_02_categorias_rubros.csv`  
**Filas:** 14 | **Columnas:** 12

Facturación por categoría de producto para los años 2021 a 2025, con ranking y crecimiento YoY.

**Columnas clave:** `categoria_rubro` (nombre CACE), `categoria_simplificada` (nombre corto), `facturacion_2025_mARS`, `participacion_2025_pct`, `ranking_facturacion_2025`

**Uso en Power BI:** Gráfico de participación de mercado por categoría. Comparar con mix de categorías propio en `fact_ventas_final.category_en`.

**Verificaciones:**
- [ ] `participacion_2025_pct` suma 100 (o cerca, excluyendo "Otros")
- [ ] `categoria_simplificada` no tiene valores duplicados
- [ ] Las facturaciones son crecientes año a año para la mayoría de categorías

---

### cace_03a_conversion_por_categoria
**Carpeta:** `02_cace_benchmarks/cace_03a_conversion_por_categoria.csv`  
**Filas:** 5 | **Columnas:** 6

Tasa de conversión (%) por categoría para H1 2024 y H1 2025.

**Columnas clave:** `categoria`, `tasa_conversion_H1_2024`, `tasa_conversion_H1_2025`, `variacion_pp`

**Uso en Power BI:** Línea de benchmark en gráficos de conversión por categoría.

**Verificaciones:**
- [ ] Tasas de conversión entre 0 y 10 (son porcentajes, no decimales)
- [ ] La fila "Total promedio" coincide con el promedio ponderado de las categorías

---

### cace_03b_ranking_demanda
**Carpeta:** `02_cace_benchmarks/cace_03b_ranking_demanda.csv`  
**Filas:** 10 | **Columnas:** 5

Ranking de las 10 categorías más demandadas en 2023, 2024 y 2025 por unidades.

**Columnas clave:** `ranking_2025`, `categoria`, `ranking_2024`, `ranking_2023`

**Uso en Power BI:** Visualización de evolución del ranking de categorías por popularidad.

**Verificaciones:**
- [ ] Rankings sin números repetidos dentro del mismo año
- [ ] 10 filas exactas (top 10)

---

### cace_04a_medios_pago_oferta
**Carpeta:** `02_cace_benchmarks/cace_04a_medios_pago_oferta.csv`  
**Filas:** 8 | **Columnas:** 9

Distribución de medios de pago en eCommerce argentino de 2022 a 2025.

**Columnas clave:** `medio_pago`, `tipo` (credito, debito, transferencia, efectivo), `Anual_2025_pct`, `MID_2025_pct`

**Uso en Power BI:** Comparar mix de medios de pago propio (`fact_ventas_final.medio_pago`) contra benchmark.

**Verificaciones:**
- [ ] Los porcentajes de `Anual_2025_pct` suman ~100 (ignorando nulos)
- [ ] No hay medios de pago duplicados

---

### cace_04b_financiamiento_cuotas
**Carpeta:** `02_cace_benchmarks/cace_04b_financiamiento_cuotas.csv`  
**Filas:** 5 | **Columnas:** 6

Distribución de ventas por cantidad de cuotas en 2024 y 2025.

**Columnas clave:** `plazo_cuotas` (1, 3, 6, 10, 15), `label`, `pct_ventas_2024`, `pct_ventas_2025`

**Uso en Power BI:** Comparar distribución de cuotas propia (`fact_ventas_final.nro_cuotas`) contra benchmark.

**Verificaciones:**
- [ ] `pct_ventas_2024` y `pct_ventas_2025` suman 100 cada una
- [ ] Los valores de `plazo_cuotas` coinciden con los de `fact_ventas_final.nro_cuotas`

---

### cace_05a_logistica_tipo_entrega
**Carpeta:** `02_cace_benchmarks/cace_05a_logistica_tipo_entrega.csv`  
**Filas:** 5 | **Columnas:** 6

Distribución de tipos de entrega en eCommerce argentino para 2023, 2024 y 2025.

**Columnas clave:** `tipo_entrega`, `pct_2025_anual`, `pct_2025_H1`

**Uso en Power BI:** Comparar tipo de entrega propio (`fact_ventas_final.tipo_entrega`) contra benchmark.

**Verificaciones:**
- [ ] `pct_2025_anual` suma ~100 (puede no cerrar exacto por redondeo)
- [ ] Los valores de `tipo_entrega` son comparables con los de `fact_ventas_final`

---

### cace_05b_plazos_entrega
**Carpeta:** `02_cace_benchmarks/cace_05b_plazos_entrega.csv`  
**Filas:** 6 | **Columnas:** 8

Distribución de plazos de entrega en 2023, 2024 y 2025, con apertura AMBA vs. Interior.

**Columnas clave:** `plazo_entrega` (same_day, 24hs, 48hs, semana, 15dias, mes_mas), `pct_2025_anual`, `pct_AMBA_2025`, `pct_interior_2025`

**Uso en Power BI:** Comparar plazos de entrega propios (`fact_ventas_final.plazo_entrega`) contra benchmark por zona.

**Verificaciones:**
- [ ] `pct_2025_anual` suma 100
- [ ] Los valores de `plazo_entrega` coinciden con los de `fact_ventas_final`
- [ ] `pct_AMBA_2025` y `pct_interior_2025` suman 100 cada una

---

### cace_06a_distribucion_regional
**Carpeta:** `02_cace_benchmarks/cace_06a_distribucion_regional.csv`  
**Filas:** 7 | **Columnas:** 8

Participación de cada región en la facturación total del eCommerce argentino en 2024 y 2025.

**Columnas clave:** `region`, `provincias`, `pct_facturacion_2024`, `pct_facturacion_2025`, `zona_simplificada`

**Uso en Power BI:** Comparar distribución geográfica de ventas propias (desde `dim_geografia_ar` vía `dim_clientes_ar` o `dim_sucursales_ar`) contra benchmark.

**Verificaciones:**
- [ ] `pct_facturacion_2025` suma 100
- [ ] Los valores de `region` son comparables con los de `dim_geografia_ar.region`

---

### cace_06b_perfil_comprador
**Carpeta:** `02_cace_benchmarks/cace_06b_perfil_comprador.csv`  
**Filas:** 13 | **Columnas:** 5

Perfil sociodemográfico del comprador online argentino 2025: distribución por género, NSE y rango etario.

**Columnas clave:** `variable` (genero, nse, edad), `segmento`, `pct_2025`

**Uso en Power BI:** Comparar perfil de clientes propio (`dim_clientes_ar`) contra benchmark. Por ejemplo: % por NSE propio vs. CACE.

**Verificaciones:**
- [ ] `pct_2025` suma 100 dentro de cada `variable`
- [ ] Los segmentos de `nse` y `edad` coinciden con los valores de `dim_clientes_ar`

---

### cace_07_canal_online_por_categoria
**Carpeta:** `02_cace_benchmarks/cace_07_canal_online_por_categoria.csv`  
**Filas:** 9 | **Columnas:** 6

Porcentaje del canal online sobre el total de ventas, por categoría, para H1 2024 y H1 2025.

**Columnas clave:** `categoria`, `pct_canal_online_H1_2024`, `pct_canal_online_H1_2025`, `variacion_pp`

**Uso en Power BI:** Mostrar qué porcentaje del mercado es online por categoría y comparar con el mix de canales propio.

**Verificaciones:**
- [ ] Los porcentajes están entre 0 y 100
- [ ] La fila "Total empresas BM" coincide con el promedio ponderado del resto

---

## 5. Orden de carga y relaciones

### Configuración previa en Power BI

Antes de cargar cualquier tabla, desactivar la opción **Fecha/hora automática** en Archivo → Opciones → Archivo actual → Carga de datos → Desactivar "Fecha/hora automática". Esta opción genera tablas de fechas automáticas que entran en conflicto con `dim_tiempo`.

Al cargar los CSV, configurar la **configuración regional del archivo como Inglés (EE.UU.)** en la pantalla de conexión o en las opciones de Power Query, ya que los archivos usan punto (`.`) como separador decimal.

### Orden de carga en Power BI

| # | Archivo | Carpeta | Tipo | Estado |
|---|---------|---------|------|--------|
| 1 | `001_dim_geografia_ar.csv` | 03_sinteticos | Dimensión | Sin cambio |
| 2 | `003_dim_canal_ar.csv` | 03_sinteticos | Dimensión | Sin cambio |
| 3 | `002_dim_sucursales_ar.csv` | 03_sinteticos | Dimensión | Sin cambio |
| 4 | `dim_inflacion_ipc.csv` | 04_procesados | Dimensión | Sin cambio |
| 5 | `dim_clientes_ar.csv` | 04_procesados | Dimensión | Sin cambio |
| 6 | `dim_tiempo.csv` | 04_procesados | Dimensión — **Date Table** | Recargar (2016–2024) |
| 7 | `dim_productos.csv` | 04_procesados | Dimensión | Recargar (+`categoria_es`) |
| 8 | `dim_categorias.csv` | 04_procesados | Dimensión puente | Carga nueva |
| 9 | `fact_ventas_final.csv` | 04_procesados | Tabla de hechos principal | Sin cambio |
| 10 | `fact_precios_comp.csv` | 04_procesados | Tabla de hechos secundaria | Carga nueva |
| 11 | `market_basket_reglas.csv` | 04_procesados | Analítica derivada | Carga nueva |
| 12 | `market_basket_reglas_enriquecidas.csv` | 04_procesados | Analítica derivada | Carga nueva opcional |
| 13 | `cace_01_kpis_macro.csv` | 02_cace_benchmarks | Referencia | Sin cambio |
| 14 | `cace_02_categorias_rubros.csv` | 02_cace_benchmarks | Referencia | Sin cambio |
| 15 | `cace_03a_conversion_por_categoria.csv` | 02_cace_benchmarks | Referencia | Sin cambio |
| 16 | `cace_03b_ranking_demanda.csv` | 02_cace_benchmarks | Referencia | Sin cambio |
| 17 | `cace_04a_medios_pago_oferta.csv` | 02_cace_benchmarks | Referencia | Sin cambio |
| 18 | `cace_04b_financiamiento_cuotas.csv` | 02_cace_benchmarks | Referencia | Sin cambio |
| 19 | `cace_05a_logistica_tipo_entrega.csv` | 02_cace_benchmarks | Referencia | Sin cambio |
| 20 | `cace_05b_plazos_entrega.csv` | 02_cace_benchmarks | Referencia | Sin cambio |
| 21 | `cace_06a_distribucion_regional.csv` | 02_cace_benchmarks | Referencia | Sin cambio |
| 22 | `cace_06b_perfil_comprador.csv` | 02_cace_benchmarks | Referencia | Sin cambio |
| 23 | `cace_07_canal_online_por_categoria.csv` | 02_cace_benchmarks | Referencia | Sin cambio |

### Relaciones formales a configurar en Model View

#### FactVentasFinal

| Tabla origen (lado N) | Columna | Tabla destino (lado 1) | Columna | Detección auto |
|---|---|---|---|---|
| `fact_ventas_final` | `fecha` | `dim_tiempo` | `fecha` | Automática |
| `fact_ventas_final` | `CanalID` | `dim_canal_ar` | `CanalID` | Automática |
| `fact_ventas_final` | `ClienteID` | `dim_clientes_ar` | `ClienteID` | Automática |
| `fact_ventas_final` | `SucursalID` | `dim_sucursales_ar` | `SucursalID` | Automática |
| `fact_ventas_final` | `PeriodoID` | `dim_inflacion_ipc` | `PeriodoID` | Automática |
| `fact_ventas_final` | `product_id` | `dim_productos` | `product_id` | Automática |

#### FactPreciosComp

| Tabla origen (lado N) | Columna | Tabla destino (lado 1) | Columna | Detección auto |
|---|---|---|---|---|
| `fact_precios_comp` | `fecha_relevamiento` | `dim_tiempo` | `fecha` | **Manual** (nombres distintos) |
| `fact_precios_comp` | `PeriodoID` | `dim_inflacion_ipc` | `PeriodoID` | Automática |
| `fact_precios_comp` | `CanalID` | `dim_canal_ar` | `CanalID` | Automática |
| `fact_precios_comp` | `categoria` | `dim_categorias` | `categoria_es` | **Manual** (nombres distintos) |

#### Dimensiones compartidas

| Tabla origen (lado N) | Columna | Tabla destino (lado 1) | Columna | Detección auto |
|---|---|---|---|---|
| `dim_sucursales_ar` | `GeografiaID` | `dim_geografia_ar` | `GeografiaID` | Automática |
| `dim_clientes_ar` | `GeografiaID` | `dim_geografia_ar` | `GeografiaID` | Automática |
| `dim_productos` | `categoria_es` | `dim_categorias` | `categoria_es` | Automática |

> **Nota:** las dos relaciones marcadas como **Manual** deben crearse explícitamente en Administrar relaciones porque las columnas de join tienen nombres distintos en cada tabla. Power BI no puede detectarlas automáticamente.

> Las tablas CACE y las tablas de Market Basket **no tienen relaciones formales** en el modelo. Se usan directamente en visualizaciones de comparación, recomendaciones y narrativa analítica.

### Pasos post-carga en Power BI

1. Marcar `dim_tiempo` como Date Table: seleccionar la tabla → Herramientas de tabla → Marcar como tabla de fechas → columna `fecha`.
2. Establecer todas las relaciones de la sección anterior en Model View.
3. Crear manualmente las dos relaciones con columnas de nombre distinto:
   - `fact_precios_comp[fecha_relevamiento]` → `dim_tiempo[fecha]`
   - `fact_precios_comp[categoria]` → `dim_categorias[categoria_es]`
4. Verificar en Model View que Power BI no haya creado relaciones automáticas incorrectas entre las tablas CACE y el resto del modelo.
5. Eliminar la columna `segmento_rfm` de `dim_clientes_ar` en Power Query (100% nula).
6. Convertir `fact_ventas_final.fecha` a tipo Fecha en Power Query si no se detectó automáticamente.
7. Convertir `dim_inflacion_ipc.fecha` y `fact_precios_comp.fecha_relevamiento` a tipo Fecha en Power Query.
8. Verificar en Model View que `dim_clientes_ar → fact_ventas_final` esté activa (línea sólida, no punteada).
9. Verificar que `fact_ventas_final → dim_productos` use la columna `product_id` y no `category_en` (eliminar y recrear si Power BI la detectó incorrectamente como N:N).
10. Cargar `market_basket_reglas.csv` y `market_basket_reglas_enriquecidas.csv` solo como tablas analíticas derivadas. No conectarlas automáticamente con `dim_categorias` ni con `dim_productos` salvo que se diseñe una vista específica de recomendaciones.
11. Si se usa SQL Server, tomar `sql/retailiq360_schema.sql` como referencia de nombres físicos (`DimTiempo`, `FactVentas`, `FactPreciosComp`, etc.), tipos de dato y 13 claves foráneas esperadas.

---

## 6. Verificaciones generales

Antes de publicar el informe, realizar las siguientes comprobaciones en Power BI:

**Conteo de filas**
- [ ] `fact_ventas_final`: 110.197 filas, 28 columnas
- [ ] `fact_precios_comp`: 360 filas, 12 columnas
- [ ] `dim_clientes_ar`: 10.000 filas
- [ ] `dim_tiempo`: 3.288 filas (2016-01-01 a 2024-12-31)
- [ ] `dim_productos`: 32.951 filas, 9 columnas
- [ ] `dim_categorias`: 10 filas, 2 columnas
- [ ] `dim_inflacion_ipc`: 111 filas
- [ ] `market_basket_reglas`: 4 filas, 9 columnas
- [ ] `market_basket_reglas_enriquecidas`: 4 filas, 11 columnas

**Modelo y relaciones**
- [ ] En Model View no hay relaciones cruzadas no intencionadas (Power BI puede auto-detectar relaciones incorrectas)
- [ ] Las tablas CACE **no tienen relaciones** con otras tablas (verificar que no se generaron automáticamente)
- [ ] `dim_tiempo` está marcada como Date Table (ícono de calendario en Model View)
- [ ] La relación `dim_clientes_ar → fact_ventas_final` es **activa** (línea sólida, no punteada)
- [ ] La relación `fact_ventas_final → dim_productos` usa `product_id` (no `category_en`) y es 1:N
- [ ] Las relaciones con columnas de nombre distinto existen: `fecha_relevamiento → fecha` y `categoria → categoria_es`
- [ ] Las tablas de Market Basket no crean relaciones automáticas con `dim_categorias`, `dim_productos` ni `fact_ventas_final`

**Lógica de datos**
- [ ] Al filtrar `fact_ventas_final` por `CanalID = 1` (Físico), todos los registros tienen `SucursalID` no nulo
- [ ] Al filtrar por `CanalID = 2, 3 o 4` (Online), todos los registros tienen `SucursalID` nulo
- [ ] Al filtrar por `tiene_ipc = False`, todas las fechas caen en sep–dic 2016
- [ ] `precio_venta_ars_real` es siempre menor o igual a `precio_venta_ars` (el deflactor reduce el precio)
- [ ] `fact_precios_comp.fecha_relevamiento` es siempre el día 15 de cada mes
- [ ] `dim_categorias.categoria_es` cubre exactamente las 10 categorías que aparecen en `fact_precios_comp.categoria`

**Tipos de dato**
- [ ] Fechas como tipo Date: `fact_ventas_final.fecha`, `fact_precios_comp.fecha_relevamiento`, `dim_inflacion_ipc.fecha`
- [ ] IDs como enteros: `CanalID`, `ClienteID`, `SucursalID`, `PeriodoID`, `CategoriaID`
- [ ] Precios como decimales: `precio_venta_ars`, `precio_venta_ars_real`, `precio_lista_ars`, `precio_web_ars`

**Medidas DAX básicas de validación**
- [ ] `SUMX(fact_ventas_final, [precio_venta_ars])` devuelve un número positivo (~81 millones)
- [ ] `COUNTROWS(dim_categorias)` = 10
- [ ] `COUNTROWS(dim_productos)` = 32.951

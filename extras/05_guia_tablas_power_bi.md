# Guía de tablas para Power BI — RetailIQ360

Descripción de cada tabla, sus relaciones y las verificaciones principales a realizar antes de construir el modelo.

---

## Índice

1. [Dimensiones](#1-dimensiones)
2. [Tablas de hechos](#2-tablas-de-hechos)
3. [Benchmarks CACE](#3-benchmarks-cace)
4. [Orden de carga y relaciones](#4-orden-de-carga-y-relaciones)
5. [Verificaciones generales](#5-verificaciones-generales)

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
- `provincia` / `ciudad` → referenciada por `dim_clientes_ar` (referencia no formal)
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
- `CanalID` → referenciada por `fact_ventas_base_ar.CanalID` (1:N)
- `CanalID` → referenciada por `fact_precios_comp.CanalID` (1:N)
- `nombre` → comparable con `cace_07_canal_online_por_categoria`

**Verificaciones:**
- [ ] Exactamente 4 filas, sin duplicados
- [ ] `peso_facturacion` suma exactamente 1.0
- [ ] `flag_online` contiene solo valores 0 y 1
- [ ] Los 4 `CanalID` (1, 2, 3, 4) están presentes en `fact_ventas_base_ar`

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
- `SucursalID` → referenciada por `fact_ventas_base_ar.SucursalID` (1:N)

**Verificaciones:**
- [ ] No hay `SucursalID` duplicados
- [ ] Todos los `GeografiaID` existen en `dim_geografia_ar`
- [ ] `flag_activa` contiene solo valores 0 y 1
- [ ] `fecha_apertura` tiene formato fecha válido (sin texto ni nulos)
- [ ] `m2_ventas` y `empleados` son valores positivos

---

### dim_clientes_ar
**Carpeta:** `03_sinteticos/004_dim_clientes_ar.csv`  
**Filas:** 10,000 | **Columnas:** 14

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `ClienteID` | Entero | Clave primaria |
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
| `segmento_rfm` | Texto | Segmento RFM (puede estar vacío) |
| `fecha_alta` | Fecha | Fecha de registro del cliente |

**Relaciones:**
- `ClienteID` → referenciada por `fact_ventas_base_ar.ClienteID` (1:N)
- `nse`, `genero`, `rango_edad` → comparables con `cace_06b_perfil_comprador`

> **Importante:** `dim_clientes_ar` **no tiene columna `GeografiaID`**. Sus campos `provincia`, `ciudad`, `region` y `zona` son texto autocontenido. No existe relación formal con `dim_geografia_ar` en Power BI. La única tabla con FK a `dim_geografia_ar` es `dim_sucursales_ar`.

**Verificaciones:**
- [ ] No hay `ClienteID` duplicados (deben ser 10,000 únicos)
- [ ] Todos los `ClienteID` de `fact_ventas_base_ar` existen en esta tabla
- [ ] Distribución de `nse`: ABC1 ~24%, C2 ~26%, C3 ~30%, D ~20%
- [ ] Distribución de `genero`: ~50% M y ~50% F
- [ ] `email` sin duplicados
- [ ] `fecha_alta` tiene formato fecha válido

---

### dim_inflacion_ipc
**Carpeta:** `04_procesados/dim_inflacion_ipc.csv`  
**Filas:** 111 | **Columnas:** 9

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `fecha` | Fecha | Primer día del mes (ej: 2017-01-01) |
| `ipc_nivel_general` | Decimal | Variación mensual IPC general en % |
| `ipc_alimentos_bebidas` | Decimal | Variación mensual IPC alimentos y bebidas |
| `ipc_indumentaria_calzado` | Decimal | Variación mensual IPC indumentaria |
| `ipc_equipamiento_hogar` | Decimal | Variación mensual IPC equipamiento hogar |
| `ipc_transporte` | Decimal | Variación mensual IPC transporte |
| `ipc_comunicacion` | Decimal | Variación mensual IPC comunicación |
| `anio` | Entero | Año (2017 a 2026) |
| `mes` | Entero | Mes (1 a 12) |

**Relaciones:**
- `(anio, mes)` → referenciada por `fact_ventas` mediante columna calculada `anio_mes`
- `ipc_nivel_general` → comparable con `cace_01_kpis_macro` (inflación interanual)

**Verificaciones:**
- [ ] No hay combinaciones `(anio, mes)` duplicadas
- [ ] La serie es continua de enero 2017 hasta el último mes disponible (sin huecos)
- [ ] Ningún valor nulo en `ipc_nivel_general`
- [ ] Los valores de `ipc_nivel_general` son razonables (entre -5% y 30% mensual)

---

## 2. Tablas de hechos

### fact_ventas
**Carpeta:** `04_procesados/fact_ventas.csv`  
**Filas:** 110,197 | **Columnas:** 18

Esta es la **tabla central del modelo**. Contiene las transacciones reales de Olist Brasil (2016-2018) ya procesadas con conversión de moneda y ajuste por inflación.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `order_id` | Texto | ID de la orden original de Olist |
| `product_id` | Texto | ID del producto original de Olist |
| `seller_id` | Texto | ID del vendedor original de Olist |
| `fecha` | Fecha | Fecha de la transacción |
| `anio` | Entero | Año (2016 a 2018) |
| `mes` | Entero | Mes (1 a 12) |
| `trimestre` | Entero | Trimestre (1 a 4) |
| `category_en` | Texto | Categoría del producto en inglés (72 categorías) |
| `price_brl` | Decimal | Precio en Reales brasileños (BRL) |
| `freight_brl` | Decimal | Flete en Reales brasileños (BRL) |
| `ars_por_usd` | Decimal | Tipo de cambio ARS/USD del día |
| `tipo_cambio` | Decimal | Factor de conversión BRL→ARS (ars_por_usd ÷ 3.3) |
| `price_ars` | Decimal | Precio en ARS nominal |
| `freight_ars` | Decimal | Flete en ARS nominal |
| `ipc_nivel_general` | Decimal | Variación IPC del mes |
| `indice_ipc_acum` | Decimal | Índice acumulado desde diciembre 2016 (base = 1.0) |
| `price_ars_real` | Decimal | Precio en ARS constantes (deflactado a dic-2016) |
| `tiene_ipc` | Booleano | True si tiene cobertura de IPC, False para sep-dic 2016 |

**Relaciones:**
- `(anio, mes)` → `dim_inflacion_ipc` mediante columna calculada `anio_mes`
- `category_en` → comparable con `cace_02_categorias_rubros.categoria_simplificada`

**Verificaciones:**
- [ ] 110,197 filas exactas después de la carga
- [ ] `order_id` + `product_id` no tiene duplicados (cada fila es un ítem único)
- [ ] `fecha` está entre 2016-09-02 y 2018-08-29
- [ ] `price_brl` y `price_ars` son valores positivos (sin negativos ni ceros)
- [ ] `tiene_ipc` es False solo para registros de sep-dic 2016 (267 filas)
- [ ] `indice_ipc_acum` empieza en 1.0 y es siempre creciente
- [ ] `price_ars_real` = `price_ars` / `indice_ipc_acum` (verificar fórmula)

---

### fact_ventas_base_ar
**Carpeta:** `03_sinteticos/005_fact_ventas_base_ar.csv`  
**Filas:** 150,000 | **Columnas:** 18

Transacciones sintéticas argentinas generadas con Faker y calibradas con benchmarks CACE 2025.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `VentaID` | Entero | Clave primaria |
| `ClienteID` | Entero | FK → `dim_clientes_ar` |
| `CanalID` | Entero | FK → `dim_canal_ar` |
| `SucursalID` | Entero | FK → `dim_sucursales_ar` (nulo si es online puro) |
| `fecha` | Fecha | Fecha de la transacción |
| `anio` | Entero | Año |
| `mes` | Entero | Mes |
| `trimestre` | Entero | Trimestre |
| `medio_pago` | Texto | Medio de pago (calibrado CACE) |
| `nro_cuotas` | Entero | Número de cuotas (calibrado CACE) |
| `tipo_entrega` | Texto | envio_domicilio, retiro_punto_venta, etc. |
| `plazo_entrega` | Texto | same_day, 24hs, 48hs, en_semana, etc. |
| `evento_comercial` | Texto | Hot Sale, Cyber Monday, etc. (puede ser nulo) |
| `precio_venta_ars` | Decimal | Precio de venta en ARS |
| `costo_unitario_ars` | Decimal | Costo del producto en ARS |
| `cantidad` | Entero | Unidades vendidas |
| `ProductoID` | Entero | FK → dimensión de producto (puede no estar cargada) |
| `TiempoID` | Entero | FK → dimensión de tiempo (puede no estar cargada) |

**Relaciones:**
- `ClienteID` → `dim_clientes_ar.ClienteID` (N:1)
- `CanalID` → `dim_canal_ar.CanalID` (N:1)
- `SucursalID` → `dim_sucursales_ar.SucursalID` (N:1, puede ser nulo)
- `medio_pago` → comparable con `cace_04a_medios_pago_oferta`
- `tipo_entrega` → comparable con `cace_05a_logistica_tipo_entrega`
- `plazo_entrega` → comparable con `cace_05b_plazos_entrega`

**Verificaciones:**
- [ ] 150,000 filas exactas después de la carga
- [ ] No hay `VentaID` duplicados
- [ ] Todos los `ClienteID` existen en `dim_clientes_ar`
- [ ] Todos los `CanalID` existen en `dim_canal_ar` (valores 1, 2, 3 o 4)
- [ ] Los `SucursalID` no nulos existen en `dim_sucursales_ar`
- [ ] Distribución de `CanalID`: CanalID=4 (Marketplace) ~47% de las filas
- [ ] `precio_venta_ars` y `costo_unitario_ars` son positivos
- [ ] `nro_cuotas` toma valores 1, 3, 6, 10 o 15

---

### fact_precios_comp
**Carpeta:** `03_sinteticos/006_fact_precios_comp.csv`  
**Filas:** 360 | **Columnas:** 11

Precios relevados por categoría y mes, incluyendo precio propio y precio de competencia.

| Columna | Tipo | Descripción |
|---------|------|-------------|
| `PrecioID` | Entero | Clave primaria |
| `categoria` | Texto | Categoría de producto |
| `anio` | Entero | Año del relevamiento |
| `mes` | Entero | Mes del relevamiento |
| `fecha_relevamiento` | Fecha | Fecha del relevamiento (día 15 de cada mes) |
| `precio_lista_ars` | Decimal | Precio de lista propio en ARS |
| `precio_web_ars` | Decimal | Precio online propio en ARS |
| `precio_competencia` | Decimal | Precio promedio de competencia en ARS |
| `descuento_pct` | Decimal | Descuento aplicado (entre 0 y 1) |
| `price_index` | Decimal | Índice precio propio / precio competencia (< 1 = más barato) |
| `CanalID` | Entero | FK → `dim_canal_ar` (canal donde aplica el precio) |

**Relaciones:**
- `CanalID` → `dim_canal_ar.CanalID` (N:1)
- `categoria` → comparable con `cace_02_categorias_rubros.categoria_simplificada`
- `(anio, mes)` → vinculable con `dim_inflacion_ipc` para análisis de precios reales

**Verificaciones:**
- [ ] 360 filas exactas (30 categorías × 12 meses o equivalente)
- [ ] No hay `PrecioID` duplicados
- [ ] Todos los `CanalID` existen en `dim_canal_ar`
- [ ] `descuento_pct` está entre 0 y 1 (no hay valores negativos ni mayores a 1)
- [ ] `price_index` es positivo
- [ ] `precio_web_ars` < `precio_lista_ars` en la mayoría de los casos

---

## 3. Benchmarks CACE

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

**Uso en Power BI:** Gráfico de participación de mercado por categoría. Comparar con mix de categorías propio en `fact_ventas`.

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

**Uso en Power BI:** Comparar mix de medios de pago propio (`fact_ventas_base_ar.medio_pago`) contra benchmark.

**Verificaciones:**
- [ ] Los porcentajes de `Anual_2025_pct` suman ~100 (ignorando nulos)
- [ ] No hay medios de pago duplicados

---

### cace_04b_financiamiento_cuotas
**Carpeta:** `02_cace_benchmarks/cace_04b_financiamiento_cuotas.csv`  
**Filas:** 5 | **Columnas:** 6

Distribución de ventas por cantidad de cuotas en 2024 y 2025.

**Columnas clave:** `plazo_cuotas` (1, 3, 6, 10, 15), `label`, `pct_ventas_2024`, `pct_ventas_2025`

**Uso en Power BI:** Comparar distribución de cuotas propia (`fact_ventas_base_ar.nro_cuotas`) contra benchmark.

**Verificaciones:**
- [ ] `pct_ventas_2024` y `pct_ventas_2025` suman 100 cada una
- [ ] Los valores de `plazo_cuotas` coinciden con los de `fact_ventas_base_ar.nro_cuotas`

---

### cace_05a_logistica_tipo_entrega
**Carpeta:** `02_cace_benchmarks/cace_05a_logistica_tipo_entrega.csv`  
**Filas:** 5 | **Columnas:** 6

Distribución de tipos de entrega en eCommerce argentino para 2023, 2024 y 2025.

**Columnas clave:** `tipo_entrega`, `pct_2025_anual`, `pct_2025_H1`

**Uso en Power BI:** Comparar tipo de entrega propio (`fact_ventas_base_ar.tipo_entrega`) contra benchmark.

**Verificaciones:**
- [ ] `pct_2025_anual` suma ~100 (puede no cerrar exacto por redondeo)
- [ ] Los valores de `tipo_entrega` son comparables con los de `fact_ventas_base_ar`

---

### cace_05b_plazos_entrega
**Carpeta:** `02_cace_benchmarks/cace_05b_plazos_entrega.csv`  
**Filas:** 6 | **Columnas:** 8

Distribución de plazos de entrega en 2023, 2024 y 2025, con apertura AMBA vs. Interior.

**Columnas clave:** `plazo_entrega` (same_day, 24hs, 48hs, semana, 15dias, mes_mas), `pct_2025_anual`, `pct_AMBA_2025`, `pct_interior_2025`

**Uso en Power BI:** Comparar plazos de entrega propios (`fact_ventas_base_ar.plazo_entrega`) contra benchmark por zona.

**Verificaciones:**
- [ ] `pct_2025_anual` suma 100
- [ ] Los valores de `plazo_entrega` coinciden con los de `fact_ventas_base_ar`
- [ ] `pct_AMBA_2025` y `pct_interior_2025` suman 100 cada una

---

### cace_06a_distribucion_regional
**Carpeta:** `02_cace_benchmarks/cace_06a_distribucion_regional.csv`  
**Filas:** 7 | **Columnas:** 8

Participación de cada región en la facturación total del eCommerce argentino en 2024 y 2025.

**Columnas clave:** `region`, `provincias`, `pct_facturacion_2024`, `pct_facturacion_2025`, `zona_simplificada`

**Uso en Power BI:** Comparar distribución geográfica de ventas propias (desde `dim_geografia_ar` + `fact_ventas_base_ar`) contra benchmark.

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

## 4. Orden de carga y relaciones

### Orden de carga en Power BI

| # | Archivo | Carpeta | Tipo |
|---|---------|---------|------|
| 1 | `001_dim_geografia_ar.csv` | 03_sinteticos | Dimensión |
| 2 | `003_dim_canal_ar.csv` | 03_sinteticos | Dimensión |
| 3 | `dim_inflacion_ipc.csv` | 04_procesados | Dimensión |
| 4 | `002_dim_sucursales_ar.csv` | 03_sinteticos | Dimensión |
| 5 | `004_dim_clientes_ar.csv` | 03_sinteticos | Dimensión |
| 6 | `fact_ventas.csv` | 04_procesados | Tabla de hechos |
| 7 | `005_fact_ventas_base_ar.csv` | 03_sinteticos | Tabla de hechos |
| 8 | `006_fact_precios_comp.csv` | 03_sinteticos | Tabla de hechos |
| 9 | `cace_01_kpis_macro.csv` | 02_cace_benchmarks | Referencia |
| 10 | `cace_02_categorias_rubros.csv` | 02_cace_benchmarks | Referencia |
| 11 | `cace_03a_conversion_por_categoria.csv` | 02_cace_benchmarks | Referencia |
| 12 | `cace_03b_ranking_demanda.csv` | 02_cace_benchmarks | Referencia |
| 13 | `cace_04a_medios_pago_oferta.csv` | 02_cace_benchmarks | Referencia |
| 14 | `cace_04b_financiamiento_cuotas.csv` | 02_cace_benchmarks | Referencia |
| 15 | `cace_05a_logistica_tipo_entrega.csv` | 02_cace_benchmarks | Referencia |
| 16 | `cace_05b_plazos_entrega.csv` | 02_cace_benchmarks | Referencia |
| 17 | `cace_06a_distribucion_regional.csv` | 02_cace_benchmarks | Referencia |
| 18 | `cace_06b_perfil_comprador.csv` | 02_cace_benchmarks | Referencia |
| 19 | `cace_07_canal_online_por_categoria.csv` | 02_cace_benchmarks | Referencia |

### Relaciones formales a configurar en Model View

| Tabla origen | Columna | Tabla destino | Columna | Cardinalidad |
|---|---|---|---|---|
| `dim_sucursales_ar` | `GeografiaID` | `dim_geografia_ar` | `GeografiaID` | N:1 |
| `fact_ventas_base_ar` | `ClienteID` | `dim_clientes_ar` | `ClienteID` | N:1 |
| `fact_ventas_base_ar` | `CanalID` | `dim_canal_ar` | `CanalID` | N:1 |
| `fact_ventas_base_ar` | `SucursalID` | `dim_sucursales_ar` | `SucursalID` | N:1 |
| `fact_precios_comp` | `CanalID` | `dim_canal_ar` | `CanalID` | N:1 |
| `fact_ventas` | `anio_mes`* | `dim_inflacion_ipc` | `anio_mes`* | N:1 |

*Columna calculada a crear: `anio_mes = FORMAT([anio], "0000") & "-" & FORMAT([mes], "00")`

> **Nota importante:** `dim_clientes_ar` **no se relaciona formalmente con `dim_geografia_ar`**. La tabla de clientes tiene los campos geográficos (`provincia`, `ciudad`, `region`, `zona`) como texto autocontenido, sin columna `GeografiaID`. La única tabla con FK hacia `dim_geografia_ar` es `dim_sucursales_ar`.

> Las tablas CACE **no tienen relaciones formales** en el modelo. Se usan directamente en visualizaciones de comparación.

---

## 5. Verificaciones generales

Antes de publicar el informe, realizar las siguientes comprobaciones en Power BI:

- [ ] El total de filas de cada tabla coincide con los valores documentados
- [ ] En Model View no hay relaciones cruzadas no intencionadas (Power BI puede auto-detectar relaciones incorrectas)
- [ ] Las tablas CACE **no tienen relaciones** con otras tablas (verificar que no se generaron automáticamente)
- [ ] Al filtrar por `CanalID = 4` en `fact_ventas_base_ar`, el resultado representa ~47% del total
- [ ] Al filtrar por `region = "AMBA"` en `dim_geografia_ar`, los clientes y sucursales asociadas son coherentes
- [ ] `fact_ventas` no tiene relación directa con las tablas sintéticas (son datasets independientes)
- [ ] Los tipos de dato son correctos: fechas como Date, IDs como enteros, porcentajes como decimales

# Explicación del notebook `04_ETL.ipynb`

## Objetivo del notebook

Este notebook construye el pipeline completo de ETL en un único flujo de ejecución, partiendo desde los archivos raw y las dimensiones sintéticas argentinas hasta obtener los siete archivos CSV listos para cargar en Power BI.

Las preguntas que responde son:

**¿Cuánto valía en pesos argentinos reales cada venta de Olist, considerando el tipo de cambio del día y la inflación acumulada, y cómo se distribuye ese volumen de ventas en el contexto del mercado e-commerce argentino?**

## Por qué un único notebook

El proceso de ETL fue desarrollado originalmente en dos etapas:
- `04_ET.ipynb` → construía `fact_ventas.csv` (precios en ARS + ajuste IPC)
- `05_ETL_integracion.ipynb` → leía ese CSV y le agregaba el contexto argentino

Esa estructura generaba una dependencia frágil: el segundo notebook asumía que el primero había corrido y dejado el archivo intermedio en disco. El notebook unificado elimina ese archivo intermedio — el DataFrame fluye de un bloque al siguiente sin tocarse el disco hasta el guardado final del bloque 10.

## Estructura del pipeline

### Bloque 0 — Configuración y carga

Se cargan todos los inputs de una vez al inicio: archivos raw de Olist, tipo de cambio BCRA, IPC INDEC, las cuatro dimensiones sintéticas argentinas y el archivo de precios de competencia (`006_fact_precios_comp.csv`). Si falta algún archivo el error aparece aquí, antes de que empiecen las transformaciones.

### Bloque 1 — Base de FactVentas (join Olist)

Une tres archivos Olist en cadena:

1. **orders + items (inner join):** conserva solo ventas con productos registrados. Cambia la granularidad de 1 fila = 1 orden a 1 fila = 1 ítem.
2. **+ products (left join):** agrega categoría del producto; si no hay ficha, la venta se conserva con categoría `other`.
3. **+ traducción (left join):** convierte la categoría del portugués al inglés.

Solo se incluyen órdenes en estado `delivered` porque son las que tienen un precio final registrado y representan ventas concretadas.

### Bloque 2 — Conversión BRL → ARS

Los precios de Olist están en reales brasileños. La conversión usa el tipo de cambio ARS/USD del BCRA como moneda puente:

```
tipo_cambio (ARS/BRL) = ARS/USD ÷ BRL_PER_USD
price_ars             = price_brl × tipo_cambio
```

`BRL_PER_USD = 3.3` es el promedio representativo del período 2016-2018. No existe una serie diaria de BRL/USD disponible, por eso se usa el BCRA (ARS/USD) que sí tiene cobertura diaria.

Los días sin cotización (fines de semana y feriados) se completan con **forward fill**: se usa el último valor hábil conocido. El mercado opera el feriado con la cotización del día hábil anterior.

### Bloque 3 — Ajuste por inflación (precios reales)

Construye un índice IPC acumulado a partir de las variaciones mensuales del INDEC:

- **Base:** diciembre 2016 = 1.0
- **Cada mes:** `índice_t = índice_{t-1} × (1 + ipc_t / 100)`
- **Precio real:** `price_ars_real = price_ars ÷ índice_acumulado`

Para los meses sep-dic 2016 (sin datos INDEC): `índice = 1.0` y `tiene_ipc = False`. Son ~317 filas (~0.3% del total). La columna `tiene_ipc` permite filtrarlas en el dashboard.

### Bloque 4 — Enriquecimiento con contexto argentino

Toma la base Olist (ya con precios reales en ARS) y le agrega las variables del mercado e-commerce argentino, calibradas con benchmarks CACE 2025:

| Variable | Fuente de distribución |
|----------|----------------------|
| `CanalID` | Peso de facturación por canal (CACE 2025 p.25) |
| `ClienteID` | Sorteo aleatorio del padrón DimClientesAr |
| `SucursalID` | Solo canal físico (CanalID = 1) |
| `medio_pago` | Medios de pago ofrecidos — CACE 04a MID 2023 |
| `nro_cuotas` | Financiamiento en cuotas — CACE 04b 2025 |
| `tipo_entrega` | Tipo de entrega 2025 — CACE 05a |
| `plazo_entrega` | Plazos de entrega 2024 — CACE 05b |

El resultado se guarda como **`fact_ventas_final.csv`**: la tabla de hechos principal del modelo.

### Bloque 5 — DimClientesAr: agregar GeografiaID

La tabla de clientes sintéticos tenía `provincia` y `ciudad` como texto libre pero no tenía FK a `DimGeografia`. Sin esa FK, Power BI no puede relacionar clientes con la jerarquía geográfica ni construir el mapa de calor por provincia.

El bloque aplica un join cascado:
1. Match exacto por `(provincia, ciudad)` → `GeografiaID` más específico
2. Fallback por `provincia` → primer `GeografiaID` de esa provincia

El resultado se guarda como **`dim_clientes_ar.csv`** (en `04_procesados/`).

### Bloque 6 — DimInflacionIpc: agregar PeriodoID e índice acumulado

Power BI no soporta relaciones por múltiples columnas. Para relacionar `DimInflacionIpc` con `FactVentasFinal` se agrega:
- `PeriodoID = anio × 100 + mes` (ej: octubre 2017 → 201710) — clave de relación numérica única
- `indice_ipc_acum` — índice calculado en el bloque 3, ahora incorporado a la dimensión para que sea autocontenida

El resultado reemplaza **`dim_inflacion_ipc.csv`** en `04_procesados/`.

### Bloque 7 — DimTiempo: tabla de fechas para Power BI

Power BI requiere una tabla de fechas marcada como **Date Table** para activar las funciones de inteligencia de tiempo (TOTALYTD, SAMEPERIODLASTYEAR, variación año anterior, etc.). Sin ella esas medidas DAX no funcionan.

La tabla cubre el rango completo **2016–2024** (no solo el período de Olist 2016-2018), porque también debe cubrir `fact_precios_comp` que tiene datos de 2022–2024. El rango se calcula dinámicamente como el año mínimo de `fact_ventas_final` y el año máximo entre `fact_ventas_final` y `fact_precios_comp`. Incluye atributos en español para filtros y leyendas del dashboard.

El resultado se guarda como **`dim_tiempo.csv`** (3.288 filas, 14 columnas).

### Bloque 8 — DimProductos: dimensión de productos

El dataset Olist tiene 32.951 fichas de producto con categoría (en portugués), peso y dimensiones físicas. Esta tabla permite analizar ventas por producto individual, filtrar por rango de peso o tamaño, y correlacionar el volumen del producto con el costo de flete.

Columna clave añadida: **`categoria_es`** — mapeo de las 72 categorías en inglés a las 10 categorías CACE en español, usando el diccionario `MAP_CAT_ES`. Este mapeo es necesario para relacionar `DimProductos` con `DimCategorias`.

El resultado se guarda como **`dim_productos.csv`** (32.951 filas, 9 columnas: `product_id`, `product_category_name`, `category_en`, `categoria_es`, `product_weight_g`, `product_length_cm`, `product_height_cm`, `product_width_cm`, `volumen_cm3`).

### Bloque 9 — DimCategorias y FactPreciosComp

**DimCategorias** es una tabla de 10 filas — una por categoría CACE — que actúa como puente entre `DimProductos` y `FactPreciosComp`. Sin ella, la relación entre ambas tablas sería N:N (cada tabla tiene múltiples filas por categoría), lo cual genera resultados incorrectos en Power BI. Con la tabla puente, las dos relaciones son 1:N limpias:
- `DimCategorias[categoria_es]` → `DimProductos[categoria_es]` (1:N)
- `DimCategorias[categoria_es]` → `FactPreciosComp[categoria]` (1:N)

**FactPreciosComp** se procesa para agregarle `PeriodoID = anio × 100 + mes`, consistente con `dim_inflacion_ipc.PeriodoID` y `fact_ventas_final.PeriodoID`. El archivo fuente en `03_sinteticos/` ya tenía `fecha_relevamiento` (día 15 de cada mes) que se verifica contra `dim_tiempo.fecha` para garantizar la cobertura total en el rango 2022–2024.

Los resultados se guardan como **`dim_categorias.csv`** (10 filas) y **`fact_precios_comp.csv`** (360 filas) en `04_procesados/`.

### Bloque 10 — Guardado y resumen

Guarda los siete archivos en `datos/04_procesados/` con `encoding='utf-8-sig'` (BOM UTF-8 que Excel y Power BI necesitan para leer correctamente las tildes y caracteres del español). Imprime un resumen de relaciones a configurar en Power BI.

## Archivos que genera

| Archivo | Carpeta | Descripción |
|---------|---------|-------------|
| `fact_ventas_final.csv` | `04_procesados/` | Tabla de hechos principal: 110.197 filas, 28 columnas |
| `dim_clientes_ar.csv` | `04_procesados/` | Clientes con GeografiaID incorporado: 10.000 filas, 15 columnas |
| `dim_inflacion_ipc.csv` | `04_procesados/` | IPC con PeriodoID e indice_ipc_acum: 111 filas, 11 columnas |
| `dim_tiempo.csv` | `04_procesados/` | Tabla de fechas 2016–2024: 3.288 filas, 14 columnas |
| `dim_productos.csv` | `04_procesados/` | Productos con categoria_es: 32.951 filas, 9 columnas |
| `dim_categorias.csv` | `04_procesados/` | Tabla puente 10 categorías CACE: 10 filas, 2 columnas |
| `fact_precios_comp.csv` | `04_procesados/` | Precios competencia con PeriodoID: 360 filas, 12 columnas |

## Columnas de `fact_ventas_final`

| Grupo | Columnas |
|-------|----------|
| Claves dimensionales | `VentaID`, `ClienteID`, `CanalID`, `SucursalID`, `PeriodoID` |
| Temporal | `fecha`, `anio`, `mes`, `trimestre` |
| Producto | `category_en`, `product_id` (trazabilidad → DimProductos) |
| Contexto argentino | `medio_pago`, `nro_cuotas`, `tipo_entrega`, `plazo_entrega`, `cantidad` |
| Precios originales (BRL) | `precio_venta_brl`, `flete_brl` |
| Tipo de cambio | `ars_por_usd`, `tipo_cambio` |
| Precios en ARS nominal | `precio_venta_ars`, `flete_ars` |
| Ajuste inflación | `ipc_nivel_general`, `indice_ipc_acum`, `precio_venta_ars_real`, `tiene_ipc` |
| Trazabilidad Olist | `order_id`, `product_id`, `seller_id` |

## Cómo se conecta con el resto del proyecto

`fact_ventas_final.csv` es el insumo principal del dashboard. El siguiente paso es:

1. Cargar los 7 archivos de `04_procesados/` en Power BI junto con las dimensiones de `03_sinteticos/`.
2. Marcar `DimTiempo` como Date Table (columna `fecha`) en la pestaña Herramientas de tabla.
3. Crear las relaciones en la Vista de Modelo según el esquema documentado en `05_guia_tablas_power_bi.md`.
4. Construir medidas DAX sobre `precio_venta_ars` (nominal) y `precio_venta_ars_real` (deflactado) para analizar el crecimiento real del negocio.

## Resumen en una frase

El notebook `04_ETL.ipynb` transforma datos crudos de Olist en una tabla de ventas completa con contexto argentino y genera las siete tablas del modelo de Power BI — incluyendo dimensión de productos, categorías CACE y precios de competencia — en un único flujo reproducible.

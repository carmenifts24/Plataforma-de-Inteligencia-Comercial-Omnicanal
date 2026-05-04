# Explicación del notebook `04_ETL.ipynb`

## Objetivo del notebook

Este notebook construye `fact_ventas.csv`, la tabla principal del modelo analítico. Aplica tres transformaciones en secuencia: une las tablas Olist, convierte precios de reales brasileños a pesos argentinos y ajusta esos precios por inflación.

La pregunta que responde es:

**¿Cuánto valía en pesos argentinos reales cada venta de Olist, considerando el tipo de cambio del día y la inflación acumulada?**

## Por qué se hizo

El EDA Nivel 2 demostró que los datos se podían unir correctamente. Este notebook materializa esa unión en un archivo final, listo para ser consumido por un dashboard o herramienta de análisis.

Sin este paso, los precios en BRL no serían comparables con el contexto económico argentino. Una venta de R$ 100 en septiembre de 2016 no vale lo mismo que una de R$ 100 en octubre de 2018, ni en pesos ni en términos de poder adquisitivo.

## 1. Base de FactVentas

El notebook parte de las órdenes con estado `delivered` y aplica tres joins sucesivos:

1. **orders + items (inner join):** conserva solo las ventas que tienen productos registrados.
2. **+ products (left join):** agrega categoría del producto; si no hay ficha, la venta se conserva con categoría `other`.
3. **+ traducción (left join):** convierte la categoría del portugués al inglés.

### Concepto clave: inner join vs left join

Un **inner join** conserva solo las filas con coincidencia en ambas tablas. Se usa entre órdenes e ítems porque una venta sin ítem no sirve para calcular facturación.

Un **left join** conserva todas las filas de la tabla izquierda aunque no haya coincidencia a la derecha. Se usa para productos y categorías porque no queremos perder ventas por una categoría faltante.

## 2. Conversión BRL → ARS

El dataset de tipo de cambio provee la cotización `ARS/USD` (pesos argentinos por dólar). Para convertir precios en reales brasileños a pesos argentinos se usa el dólar como moneda puente:

```text
price_ars = price_brl × (ARS/USD) ÷ (BRL/USD)
```

El valor `BRL/USD = 3.3` es un promedio representativo del período 2016-2018 (1 dólar equivalía a aproximadamente 3,3 reales).

### Concepto clave: forward fill

Las cotizaciones del dólar no existen los fines de semana ni los feriados. Para esos días se aplica **forward fill**: se usa el último valor conocido disponible.

Por ejemplo, si el viernes hay cotización y el sábado no, se usa la cotización del viernes para las ventas de ese sábado.

## 3. Ajuste por inflación (precios reales)

El IPC del INDEC registra la variación mensual de precios en Argentina. A partir de esas variaciones porcentuales se construye un **índice IPC acumulado**.

### Cómo funciona el índice

- **Base:** diciembre 2016 = 1.0
- **Cada mes:** el índice se multiplica por `(1 + variación% / 100)`
- **Ejemplo:** si enero 2017 tuvo 1.3% de inflación, el índice de enero = 1.0 × 1.013 = 1.013

Para obtener el precio real se divide el precio nominal por el índice acumulado del mes de la venta:

```text
price_ars_real = price_ars ÷ indice_ipc_acum
```

### Concepto clave: precio nominal vs precio real

El **precio nominal** es el precio expresado en pesos del momento en que ocurrió la venta.

El **precio real** es ese mismo precio expresado en pesos de un período base (en este caso, diciembre 2016), eliminando el efecto de la inflación.

Comparar precios reales permite saber si las ventas crecieron porque el negocio creció o simplemente porque los precios subieron por inflación.

### Qué pasa con los meses sin IPC

El IPC del INDEC disponible empieza en enero 2017, pero Olist tiene ventas desde septiembre 2016. Para los meses septiembre, octubre, noviembre y diciembre de 2016 se asigna `indice_ipc_acum = 1.0`, equivalente a expresar esos precios directamente en pesos diciembre 2016 sin ajuste.

Esta decisión queda registrada en la columna `tiene_ipc` (True/False), que permite identificar en análisis posteriores qué filas tienen ajuste real y cuáles no.

## 4. Columnas del archivo final

| Columna | Descripción |
|---------|-------------|
| `order_id` | Identificador de la orden |
| `product_id` | Identificador del producto |
| `seller_id` | Identificador del vendedor |
| `fecha` | Fecha de la compra (sin hora) |
| `anio`, `mes`, `trimestre` | Desgloses temporales para filtros |
| `category_en` | Categoría del producto en inglés |
| `price_brl` | Precio original en reales brasileños |
| `freight_brl` | Flete original en reales brasileños |
| `ars_por_usd` | Cotización ARS/USD del día de la venta |
| `tipo_cambio` | Tipo de cambio BRL/ARS aplicado |
| `price_ars` | Precio en pesos argentinos nominales |
| `freight_ars` | Flete en pesos argentinos nominales |
| `ipc_nivel_general` | Variación mensual IPC (%) del mes de la venta |
| `indice_ipc_acum` | Índice IPC acumulado del mes (base dic-2016 = 1.0) |
| `price_ars_real` | Precio en pesos constantes diciembre 2016 |
| `tiene_ipc` | True si el mes tiene cobertura del INDEC |

## Resultado del notebook

El notebook genera un archivo:

```text
datos/04_procesados/fact_ventas.csv
```

Con aproximadamente 110.000 filas que representan cada ítem vendido en Olist durante el período 2016-2018, con precios en BRL, ARS nominal y ARS real.

## Cómo se conecta con el resto del proyecto

`fact_ventas.csv` es el insumo principal para el dashboard y el modelado. El siguiente paso natural es:

- Conectar esta tabla a Power BI o una herramienta de visualización.
- Agregar las dimensiones sintéticas argentinas (clientes, sucursales, canales) para análisis omnicanal.
- Calcular KPIs: facturación total, ticket promedio, crecimiento real vs nominal, distribución por categoría.

## Resumen en una frase

El notebook `04_ETL.ipynb` transforma datos crudos de Olist en una tabla de ventas lista para análisis, expresada en pesos argentinos reales y organizada para responder preguntas comerciales concretas.

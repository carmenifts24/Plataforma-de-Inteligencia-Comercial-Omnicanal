# Explicación del notebook `02_EDA_nivel_1.ipynb`

## Objetivo del notebook

Este notebook realiza un EDA de nivel 1. EDA significa análisis exploratorio de datos. En esta primera etapa, el objetivo no es sacar conclusiones comerciales profundas, sino revisar si cada archivo está en condiciones mínimas para ser usado.

La pregunta principal es:

**¿Cada dataset está suficientemente limpio, completo y bien estructurado para entrar al modelo?**

## Qué significa EDA de nivel 1

Un EDA de nivel 1 es una revisión estructural. Se observa archivo por archivo para detectar problemas básicos:

- Cantidad de filas y columnas.
- Tipos de datos.
- Valores nulos.
- Duplicados.
- Columnas clave.
- Rangos de fechas.
- Valores extremos.
- Posibles problemas antes de hacer joins.

Es como hacer una inspección técnica antes de usar los datos en análisis más complejos.

## Por qué se hizo

En un proyecto de datos, los errores suelen aparecer cuando se unen tablas o se construyen métricas. Si antes no revisamos la calidad de cada archivo, podemos tomar decisiones con datos incompletos o mal interpretados.

Este notebook reduce ese riesgo. Permite decidir qué archivos están listos, cuáles requieren limpieza y qué reglas debe aplicar el futuro ETL.

## Concepto clave: ETL

ETL significa:

- Extract: extraer datos desde archivos o sistemas.
- Transform: limpiar, unir y modificar los datos.
- Load: cargar los datos finales en una base, dashboard o modelo.

Este notebook no es el ETL final, pero define decisiones que el ETL deberá respetar.

## 1. Función `diagnostico()`

El notebook empieza creando una función llamada `diagnostico()`.

Una función es un bloque de código reutilizable. En lugar de escribir el mismo análisis muchas veces para cada archivo, se define una sola función y se aplica a todos los datasets.

La función revisa:

- Dimensiones del archivo.
- Columnas y tipos de dato.
- Cantidad y porcentaje de nulos.
- Duplicados.
- Nulos en una columna clave.
- Estadísticas de columnas numéricas.
- Estado general tipo semáforo.

## Por qué se hizo

Usar una función evita repetir código y ayuda a que todos los archivos se evalúen con el mismo criterio.

Esto es importante porque si cada archivo se revisara de forma distinta, el diagnóstico final sería menos comparable.

## Concepto clave: semáforo

El semáforo es una forma simple de resumir el estado de cada archivo:

- OK: el archivo parece listo.
- Issues menores: tiene detalles, pero no bloquean el trabajo.
- Revisar: tiene alertas que deben entenderse antes de usarlo.

No todos los avisos del semáforo significan errores. Algunos son comportamientos esperados del negocio.

## 2. Revisión de `001_olist_orders_dataset.csv`

Este archivo contiene las órdenes de Olist. Es una tabla central porque muchas otras tablas se conectan a través de `order_id`.

El notebook revisa:

- Si `order_id` es único.
- La distribución de `order_status`.
- Cuántas órdenes están en estado `delivered`.
- El rango temporal de las compras.
- Valores nulos.

## Por qué se hizo

Para construir ventas reales, normalmente se usan solo órdenes entregadas. Una orden cancelada o no entregada no debería contarse igual que una venta finalizada.

El notebook decide que las órdenes `delivered` son las que entran en `FactVentas`.

## Concepto clave: clave primaria

Una clave primaria identifica de forma única una fila. En `orders`, `order_id` debería aparecer una sola vez porque cada fila representa una orden.

Si una clave primaria aparece duplicada, puede haber un problema grave de datos.

## 3. Revisión de `002_olist_order_items_dataset.csv`

Este archivo contiene los productos o ítems dentro de cada orden.

El notebook revisa:

- Si hay nulos.
- Si `order_id` aparece repetido.
- Precios iguales a cero.
- Precios negativos.
- Precios muy altos.
- Cantidad de ítems por orden.

## Por qué se hizo

En este archivo, que `order_id` se repita no es un error. Una misma orden puede tener varios productos.

La decisión importante es que la granularidad de `FactVentas` será:

```text
1 fila = 1 ítem vendido
```

Esto permite analizar ventas con más detalle que si se usara una fila por orden.

## Concepto clave: granularidad

La granularidad indica qué representa cada fila de una tabla.

Ejemplos:

- Una fila por cliente.
- Una fila por orden.
- Una fila por producto vendido.
- Una fila por mes.

Definir la granularidad es fundamental porque afecta todas las métricas posteriores.

## 4. Revisión de `003_olist_order_payments_dataset.csv`

Este archivo contiene pagos de Olist.

El notebook revisa:

- Cobertura contra `orders`.
- Repetición de `order_id`.
- Tipos de pago disponibles.

## Por qué se hizo

El notebook concluye que los pagos brasileños no se usarán directamente, porque el proyecto quiere representar una operación argentina. Por eso, los medios de pago serán reemplazados por columnas generadas con datos sintéticos argentinos.

De todos modos, revisar este archivo sirve para saber si las órdenes tienen información de pago asociada y para entender qué se está descartando.

## 5. Revisión de `004_olist_products_dataset.csv` y `005_product_category_name_translation.csv`

Estos archivos se usan para construir la dimensión de producto.

El notebook revisa:

- Si `product_id` es único.
- Categorías faltantes.
- Traducciones disponibles.
- Categorías más frecuentes.

## Por qué se hizo

Olist trae categorías en portugués. El archivo de traducción permite pasarlas a inglés. En un ETL posterior podrían mapearse a español o agruparse en categorías comerciales propias.

La decisión documentada es que los productos sin categoría pueden agruparse como "Otros".

## Concepto clave: lookup

Una tabla lookup es una tabla auxiliar que sirve para traducir, clasificar o completar información.

En este caso, `product_category_name_translation.csv` funciona como lookup para traducir categorías.

## 6. Revisión de `006_Sample - Superstore.csv`

Este dataset se usa como referencia comercial para márgenes y descuentos.

El notebook revisa:

- Ventas.
- Ganancia o pérdida.
- Descuentos.
- Margen promedio.
- Categorías y subcategorías.

## Por qué se hizo

El proyecto necesita valores comerciales realistas para analizar precios y rentabilidad. Superstore aporta una referencia útil para calibrar márgenes y descuentos.

La decisión es usar este dataset para alimentar o calibrar `FactPreciosComp`.

## Concepto clave: margen

El margen indica cuánto queda de ganancia en relación con la venta.

Una forma simple de pensarlo:

```text
margen = ganancia / venta
```

Si una venta tiene margen negativo, significa que se vendió con pérdida.

## 7. Revisión y procesamiento de `007_sh_ipc_aperturas.xls`

Este archivo contiene datos de IPC del INDEC. Es el archivo más complejo porque viene en formato Excel con encabezados y filas especiales.

El notebook hace varios pasos:

1. Lee el archivo crudo para entender su estructura.
2. Identifica qué fila contiene los encabezados.
3. Selecciona rubros específicos.
4. Transpone la tabla.
5. Convierte fechas.
6. Agrega año y mes.
7. Guarda el resultado limpio como `dim_inflacion_ipc.csv`.

## Por qué se hizo

El IPC permite ajustar precios por inflación. En Argentina, comparar precios nominales sin considerar inflación puede llevar a conclusiones engañosas.

Por ejemplo, vender más pesos en 2024 que en 2022 no necesariamente significa vender más en términos reales. Parte de ese aumento puede deberse a inflación.

## Concepto clave: transponer

Transponer una tabla significa intercambiar filas y columnas.

En este caso, el Excel original tenía rubros como filas y fechas como columnas. Para análisis posterior, conviene que cada fila sea una fecha y las columnas sean los rubros de inflación.

## 8. Revisión de `008_tipos-de-cambio-historicos.csv`

Este archivo contiene series de tipo de cambio.

El notebook revisa:

- Columnas disponibles.
- Porcentaje de datos no nulos por columna.
- Cobertura temporal.
- Cobertura durante el período de Olist.
- Columna elegida para trabajar.

La columna seleccionada es:

```text
dolar_estadounidense
```

## Por qué se hizo

El tipo de cambio permite analizar precios o ventas en moneda dura, por ejemplo en dólares. Esto puede ser útil cuando hay inflación o devaluaciones.

El notebook detecta que muchas columnas tienen muchísimos nulos, por eso no alcanza con mirar el porcentaje total de nulos: hay que elegir la columna realmente útil.

## 9. Revisión de `009_olist_order_reviews_dataset.csv`

Este archivo contiene reseñas de clientes.

El notebook revisa:

- Puntajes de satisfacción.
- Nulos.
- Duplicados por `order_id`.
- Distribución de `review_score`.

## Por qué se hizo

Las reseñas no son parte obligatoria del modelo principal, pero pueden enriquecer el dashboard con indicadores de satisfacción.

Por ejemplo:

- Score promedio.
- Relación entre retrasos logísticos y baja calificación.
- Categorías con mejores o peores reseñas.

## 10. Semáforo final

Al final, el notebook arma una tabla consolidada con el diagnóstico de todos los archivos y una lista de decisiones para el ETL.

Algunas decisiones importantes son:

- Usar solo órdenes `delivered`.
- Revisar órdenes sin ítems antes del join.
- Descartar medios de pago brasileños y reemplazarlos con una capa argentina.
- Usar traducción de categorías como lookup.
- Usar Superstore para márgenes.
- Usar IPC procesado para inflación.
- Usar `dolar_estadounidense` como tipo de cambio.
- Considerar reviews como dato opcional.

## Resultado del notebook

El principal resultado es una guía de calidad y decisiones para preparar los datos.

Además, el notebook genera un archivo procesado:

```text
datos/04_procesados/dim_inflacion_ipc.csv
```

## Cómo se conecta con el resto del proyecto

Este notebook prepara la base para el EDA de nivel 2 y para el futuro ETL. El nivel 1 mira cada archivo por separado. El nivel 2 revisa cómo se comportan los archivos cuando se relacionan entre sí.

## Resumen en una frase

El notebook `02_EDA_nivel_1.ipynb` se hizo para revisar la calidad estructural de cada dataset, documentar problemas esperados y definir reglas claras para la integración posterior de datos.

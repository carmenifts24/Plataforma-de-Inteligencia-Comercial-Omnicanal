# Explicación del notebook `03_EDA_nivel_2.ipynb`

## Objetivo del notebook

Este notebook realiza un EDA de nivel 2. A diferencia del EDA de nivel 1, que revisa cada archivo por separado, este notebook analiza si los datos son coherentes entre sí.

La pregunta principal es:

**¿Las tablas se pueden unir sin perder información importante ni generar errores de interpretación?**

## Qué significa EDA de nivel 2

El EDA de nivel 2 mira relaciones entre datasets:

- Si las órdenes tienen ítems.
- Si los ítems tienen productos.
- Si las fechas de ventas tienen cobertura de IPC.
- Si las fechas de ventas tienen cobertura de tipo de cambio.
- Si las categorías de distintos datasets pueden mapearse.
- Si una primera base de `FactVentas` puede construirse correctamente.

Este nivel ya se acerca más al diseño real del modelo de datos.

## Por qué se hizo

En proyectos de datos, un archivo puede estar bien por separado pero fallar al combinarse con otros.

Por ejemplo:

- Una orden puede existir en `orders`, pero no tener ítems en `items`.
- Un producto puede aparecer vendido, pero no tener ficha en `products`.
- Una fecha de venta puede no tener IPC disponible.
- Una categoría puede existir en Olist pero no tener equivalencia clara con Superstore.

Este notebook busca encontrar esos problemas antes de construir el ETL definitivo.

## 1. Configuración y carga de datos

El notebook carga archivos desde tres carpetas:

- `datos/01_raw`, para datos originales.
- `datos/04_procesados`, para datos ya limpiados, como IPC.
- `datos/02_cace_benchmarks`, para benchmarks de CACE.

Carga datasets de:

- Olist orders.
- Olist items.
- Olist products.
- Traducción de categorías.
- Superstore.
- IPC procesado.
- Tipo de cambio histórico.

También convierte fechas y filtra las órdenes con estado `delivered`.

## Por qué se hizo

El notebook se diseña para no depender de resultados guardados en memoria por notebooks anteriores. Carga todo desde cero para que sea más confiable.

Filtrar órdenes `delivered` mantiene la misma decisión tomada en el EDA de nivel 1: solo se consideran ventas efectivamente entregadas para la base principal.

## Concepto clave: independencia del notebook

Un notebook es más confiable cuando puede ejecutarse desde cero sin depender de que otro notebook haya dejado variables cargadas en memoria.

Eso evita errores difíciles de detectar.

## 2. Integridad entre `orders` e `items`

El notebook compara:

- Órdenes entregadas en `orders`.
- Órdenes que aparecen en `items`.

Busca dos problemas:

- Órdenes entregadas sin ítems.
- Ítems con `order_id` que no existe en `orders`.

## Por qué se hizo

Para construir una tabla de ventas, necesitamos unir órdenes con productos vendidos. Si una orden no tiene ítems, no se puede calcular qué se vendió ni por cuánto.

Si un ítem tiene una orden inexistente, también hay un problema de integridad.

## Concepto clave: integridad referencial

La integridad referencial significa que las relaciones entre tablas son válidas.

Ejemplo:

Si una tabla de ítems dice que un producto pertenece a la orden `123`, entonces la orden `123` debería existir en la tabla de órdenes.

## 3. Integridad entre `items` y `products`

El notebook compara:

- `product_id` presentes en los ítems vendidos.
- `product_id` existentes en la tabla de productos.

Busca productos vendidos que no tengan ficha de producto.

## Por qué se hizo

Si un ítem vendido no tiene información de producto, se puede perder categoría, dimensiones u otra información útil.

El notebook propone una decisión de ETL: usar `left join` y completar categoría como "Sin ficha" si faltara información.

## Concepto clave: join

Un join es una unión entre tablas usando una columna en común.

Ejemplo:

- `orders` tiene `order_id`.
- `items` también tiene `order_id`.
- Se pueden unir para saber qué productos pertenecen a cada orden.

## Concepto clave: `inner join` y `left join`

Un `inner join` conserva solo las filas que tienen coincidencia en ambas tablas.

Un `left join` conserva todas las filas de la tabla izquierda, aunque no encuentre coincidencia en la derecha.

En este proyecto:

- `inner join` se usa entre órdenes entregadas e ítems porque una venta sin ítem no sirve para calcular facturación por producto.
- `left join` se usa para productos y traducciones porque conviene no perder ventas si falta una categoría o traducción.

## 4. Distribución temporal de ventas

El notebook agrupa órdenes entregadas por año y mes.

Luego identifica:

- Mes con más ventas.
- Mes con menos ventas.
- Volumen mensual de órdenes.

## Por qué se hizo

Antes de analizar inflación o tipo de cambio, hay que conocer el período real de ventas.

También sirve para detectar meses raros, por ejemplo meses incompletos o con muy pocas órdenes.

## 5. Ticket promedio y distribución de precios

El notebook une órdenes entregadas con ítems y calcula el ticket por orden.

Luego muestra:

- Ticket promedio.
- Ticket mediano.
- Ticket mínimo.
- Ticket máximo.
- Distribución por rangos de precio.

## Por qué se hizo

El ticket promedio ayuda a entender el valor típico de una orden. La mediana también es importante porque los promedios pueden distorsionarse por valores extremos.

Por ejemplo, unas pocas órdenes muy caras pueden subir el promedio, aunque la mayoría de las órdenes sean más pequeñas.

## Concepto clave: promedio y mediana

El promedio suma todos los valores y divide por la cantidad de casos.

La mediana es el valor del medio cuando los datos están ordenados.

La mediana suele ser más robusta cuando hay valores extremos.

## 6. Cobertura del IPC

El notebook compara los meses con ventas Olist contra los meses disponibles en la tabla `dim_inflacion_ipc.csv`.

Si faltan meses, los muestra y cuenta cuántas órdenes afectadas hay.

## Por qué se hizo

Para ajustar ventas por inflación, cada mes de venta debería tener un dato de IPC. Si hay meses sin IPC, el ETL debe decidir qué hacer.

El notebook sugiere dos alternativas:

- Usar IPC igual a 0 para esos meses, sin ajuste.
- Imputar con el primer valor disponible.

## Concepto clave: imputar

Imputar significa completar un dato faltante usando una regla.

Ejemplo: si falta el IPC de septiembre de 2016, se podría usar el primer IPC disponible como aproximación.

## 7. Cobertura del tipo de cambio

El notebook compara los días con órdenes Olist contra los días que tienen cotización de dólar estadounidense.

Detecta fechas sin cotización y explica que pueden corresponder a fines de semana o feriados.

## Por qué se hizo

Si se quiere convertir ventas a dólares, cada fecha de venta necesita un tipo de cambio. Pero las cotizaciones no siempre existen todos los días.

La decisión sugerida es aplicar `forward fill`, es decir, usar el último valor conocido.

## Concepto clave: forward fill

Forward fill significa rellenar un dato faltante con el último valor disponible anterior.

Ejemplo:

Si el viernes hay cotización y el sábado no, se usa la cotización del viernes.

Esto es habitual en series financieras cuando no hay datos en fines de semana o feriados.

## 8. Comparación de categorías Olist vs Superstore

El notebook muestra las principales categorías de Olist y las categorías de Superstore.

Luego sugiere un mapeo aproximado, por ejemplo:

- Technology / Phones hacia telefonía.
- Technology / Computers hacia informática y accesorios.
- Furniture hacia muebles y decoración.
- Office Supplies hacia utilidades domésticas.

## Por qué se hizo

Olist y Superstore no usan las mismas categorías. Si se quiere usar Superstore para márgenes o referencias comerciales, hay que encontrar equivalencias razonables.

Este paso no resuelve todo el mapeo, pero deja una guía para el ETL.

## Concepto clave: mapeo de categorías

Mapear categorías significa establecer equivalencias entre nombres de distintas fuentes.

Por ejemplo, una fuente puede decir "Technology" y otra "Electrónica". Para analizarlas juntas, necesitamos decidir si representan el mismo grupo comercial.

## 9. Vista rápida de archivos CACE

El notebook lista los archivos CACE disponibles y muestra KPIs macro.

## Por qué se hizo

CACE aporta contexto argentino sobre comercio electrónico:

- Canales.
- Medios de pago.
- Logística.
- Conversión.
- Distribución regional.
- Categorías.

Estos benchmarks permiten calibrar los datos sintéticos y justificar decisiones del modelo.

## 10. Construcción de una base preliminar de `FactVentas`

El notebook construye una tabla base paso a paso:

1. Parte de órdenes `delivered`.
2. Une con ítems.
3. Une con productos.
4. Une con traducción de categorías.
5. Completa categorías faltantes como `other`.
6. Agrega columnas de año, mes y fecha diaria.

## Por qué se hizo

Este bloque demuestra que la tabla principal de ventas puede construirse.

No es todavía el ETL final, pero es una prueba de concepto: confirma que las relaciones principales funcionan y que se puede obtener una base útil para análisis.

## 11. Resumen final

El notebook muestra:

- Primeras filas de la base.
- Total de ítems en `FactVentas`.
- Órdenes únicas.
- Facturación total en reales brasileños.
- Cantidad de categorías distintas.
- Período cubierto.

## Por qué se hizo

Este resumen permite validar que el resultado final tiene sentido antes de avanzar.

Si el número de filas fuera inesperadamente bajo, si la facturación fuera cero o si no hubiera categorías, eso indicaría un problema en los joins.

## Resultado del notebook

Este notebook no genera archivos nuevos. Su resultado principal es una validación funcional:

- Las tablas principales pueden relacionarse.
- Se identifican decisiones necesarias para IPC y tipo de cambio.
- Se propone un camino para mapear categorías.
- Se construye una base preliminar de ventas.

## Cómo se conecta con el resto del proyecto

El EDA de nivel 2 es el puente entre diagnóstico y construcción del modelo.

Después de este notebook, el siguiente paso natural es crear un ETL formal que:

- Construya `FactVentas`.
- Integre productos, clientes, canales y fechas.
- Convierta monedas si corresponde.
- Ajuste precios por inflación.
- Prepare datos para Power BI o dashboard.

## Resumen en una frase

El notebook `03_EDA_nivel_2.ipynb` se hizo para comprobar que los datasets se conectan correctamente entre sí y que existe una ruta clara para construir la tabla principal de ventas del proyecto.

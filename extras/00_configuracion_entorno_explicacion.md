# Explicación del notebook `00_configuracion_entorno.ipynb`

## Objetivo del notebook

Este notebook funciona como la puerta de entrada del proyecto. Su objetivo principal es comprobar que el entorno de trabajo está listo para analizar datos: que Python funciona, que las librerías necesarias están instaladas y que los archivos de datos se pueden leer correctamente.

En palabras simples: antes de construir análisis, gráficos o modelos, este notebook responde la pregunta **"¿tengo todo preparado para trabajar sin problemas?"**.

## Qué se hizo

### 1. Se verificó el entorno de Python

El notebook importa librerías muy usadas en ciencia de datos:

- `pandas`, para trabajar con tablas.
- `numpy`, para cálculos numéricos.
- `matplotlib`, `seaborn` y `plotly`, para gráficos.
- `sklearn`, para tareas de machine learning.

Después imprime las versiones instaladas. Esto es importante porque dos personas pueden tener el mismo código, pero si usan versiones muy distintas de las librerías, el resultado puede cambiar o incluso aparecer errores.

## Por qué se hizo

En proyectos de datos, el entorno es parte del proyecto. Si no sabemos qué versiones de herramientas estamos usando, es más difícil repetir el análisis en otra computadora o explicar por qué algo funciona en un equipo y falla en otro.

Este paso ayuda a asegurar reproducibilidad, es decir, que otra persona pueda abrir el proyecto y obtener resultados similares.

## Concepto clave: librería

Una librería es un conjunto de herramientas ya programadas por otras personas. Por ejemplo, `pandas` permite leer archivos CSV y trabajar con tablas sin tener que programar todo desde cero.

Es parecido a usar una calculadora especializada: no construimos la calculadora, solo la usamos para resolver el problema.

## 2. Se configuró cómo se muestran los datos y gráficos

El notebook ajusta opciones visuales:

- Tamaño de los gráficos.
- Tamaño de títulos y etiquetas.
- Estilo visual de `seaborn`.
- Cantidad máxima de columnas y filas que muestra `pandas`.
- Formato de números decimales.

## Por qué se hizo

Estos ajustes no cambian los datos. Cambian la forma en que los vemos.

Cuando se trabaja en notebooks, la claridad visual es muy importante. Si una tabla se corta demasiado, si un gráfico sale muy pequeño o si los números aparecen con demasiados decimales, el análisis se vuelve más difícil de leer.

Este bloque busca que el notebook sea más cómodo para explorar información.

## 3. Se hizo un inventario de archivos disponibles

El notebook intenta recorrer una carpeta de datos y listar archivos CSV, Excel o XLS. Para cada archivo calcula:

- Nombre.
- Extensión.
- Tamaño en kilobytes.

## Por qué se hizo

Antes de analizar datos, conviene saber qué archivos existen. Este inventario sirve como primer control de organización.

Es como revisar qué ingredientes hay en la cocina antes de empezar una receta.

## Rutas del proyecto

Los datos están organizados en:

```text
datos/01_raw               ← datos originales sin modificar
datos/02_cace_benchmarks   ← benchmarks CACE
datos/03_sinteticos        ← datos generados por el notebook 01
datos/04_procesados        ← outputs del EDA listos para ETL
```

Los notebooks usan rutas relativas como `../datos/01_raw` desde la carpeta `notebooks/`.

## 4. Se hizo una vista previa de Olist Orders

El notebook lee el archivo de órdenes de Olist y muestra:

- Cantidad de filas y columnas.
- Lista de columnas.
- Primeras filas.
- Tipos de datos.
- Valores nulos por columna.

## Por qué se hizo

`olist_orders_dataset.csv` es uno de los archivos centrales del proyecto porque contiene las órdenes de compra. Antes de unirlo con otros archivos, hay que entender su estructura.

Las preguntas iniciales son:

- ¿Cuántas órdenes hay?
- ¿Qué columnas tiene?
- ¿Hay fechas?
- ¿Hay valores faltantes?
- ¿Qué significa cada columna?

## Concepto clave: valores nulos

Un valor nulo es un dato faltante. Por ejemplo, una orden puede no tener fecha de entrega si fue cancelada o si nunca llegó a completarse.

Los nulos no siempre son errores. A veces representan algo real. Lo importante es entender por qué están ahí.

## 5. Se hizo una vista previa de Sample Superstore

El notebook también lee el dataset `Sample - Superstore.csv`, usando `encoding='latin-1'`.

## Por qué se hizo

Este archivo contiene información comercial como ventas, descuentos y rentabilidad. En el proyecto se usa como referencia para entender márgenes, descuentos y comportamiento de retail.

El parámetro `encoding='latin-1'` se usa porque algunos CSV tienen caracteres especiales y no siempre están guardados con la codificación estándar `utf-8`.

## Concepto clave: encoding

El encoding es la forma en que una computadora interpreta letras, tildes, símbolos y caracteres especiales dentro de un archivo.

Si el encoding es incorrecto, pueden aparecer caracteres raros o errores al leer el archivo. Por eso a veces se prueba con `latin-1`.

## Resultado del notebook

Este notebook no crea archivos nuevos ni modifica datos. Su resultado es un diagnóstico inicial:

- Confirma si las librerías principales están instaladas.
- Configura la visualización.
- Lista archivos disponibles.
- Abre datasets importantes para revisar que se puedan leer.

## Cómo se conecta con el resto del proyecto

Este notebook prepara el terreno. Después de verificar que el entorno y los archivos funcionan, el proyecto avanza hacia tareas más profundas:

- Generar datos sintéticos argentinos.
- Diagnosticar calidad de cada archivo.
- Validar relaciones entre tablas.
- Preparar un futuro ETL y dashboard.

## Resumen en una frase

El notebook `00_configuracion_entorno.ipynb` se hizo para asegurarse de que la computadora, las librerías y los datos básicos están listos antes de avanzar con análisis más complejos.

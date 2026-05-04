# Explicación del notebook `01_creador_datos_sinteticos.ipynb`

## Objetivo del notebook

Este notebook crea datos sintéticos, es decir, datos ficticios pero realistas. Su objetivo es agregar una capa argentina al proyecto RetailIQ 360°, porque los datasets originales no alcanzan por sí solos para representar una operación omnicanal argentina.

Olist trae datos reales de e-commerce brasileño y Superstore trae datos comerciales de referencia, pero faltaban elementos como:

- Provincias y ciudades argentinas.
- Sucursales argentinas.
- Clientes con distribución regional argentina.
- Canales de venta locales.
- Medios de pago y tipos de entrega acordes al comercio electrónico argentino.
- Eventos comerciales como Hot Sale, CyberMonday o Navidad.
- Precios de competencia en pesos argentinos.

## Qué significa "datos sintéticos"

Los datos sintéticos son datos creados artificialmente. No pertenecen a personas reales ni a ventas reales, pero se generan siguiendo reglas para que se parezcan a un escenario posible.

En este proyecto se usan porque permiten construir y probar un modelo de análisis completo sin exponer datos privados de clientes o empresas.

## Por qué se hizo

El proyecto busca simular una plataforma de inteligencia comercial omnicanal. Para eso no alcanza con tener ventas: también se necesita contexto.

Por ejemplo, para analizar ventas por región, necesitamos saber en qué provincia vive cada cliente. Para analizar logística, necesitamos tipos de entrega. Para analizar canales, necesitamos distinguir tienda física, web, app y marketplace.

Este notebook crea esas piezas faltantes.

## 1. Instalación y verificación de herramientas

El notebook instala y verifica librerías:

- `faker`, para crear nombres, emails, teléfonos y empresas ficticias.
- `pandas`, para construir tablas.
- `numpy`, para generar valores aleatorios con probabilidades.

## Por qué se hizo

`Faker` permite generar datos humanos realistas sin usar datos reales. Por ejemplo, puede crear nombres, correos y teléfonos con formato argentino.

Esto es útil para que las tablas se vean parecidas a las que tendría una empresa real, pero sin comprometer información sensible.

## 2. Configuración de semilla aleatoria

El notebook define:

```python
SEED = 42
```

También configura esa semilla en `random`, `numpy` y `Faker`.

## Por qué se hizo

Cuando se generan datos aleatorios, normalmente cambian cada vez que se ejecuta el código. La semilla hace que el azar sea repetible.

Esto significa que, si otra persona corre el notebook, debería obtener los mismos datos. Para un proyecto académico o profesional, esto es muy importante porque permite explicar, revisar y reproducir el trabajo.

## Concepto clave: semilla

Una semilla es un punto de partida para generar números aleatorios. No elimina el azar, pero lo vuelve controlado.

Es como decirle al programa: "genera datos al azar, pero hazlo siempre siguiendo la misma secuencia".

## 3. Definición de provincias, ciudades y regiones argentinas

El notebook crea una estructura con regiones como:

- AMBA.
- Litoral.
- Centro.
- Sur.
- NOA.
- Cuyo.

Dentro de cada región se definen provincias, ciudades y pesos de facturación inspirados en datos de CACE 2025.

## Por qué se hizo

No todas las regiones tienen el mismo peso comercial. AMBA, por ejemplo, suele concentrar más actividad que otras zonas.

Usar pesos permite que los datos sintéticos no queden distribuidos de forma artificialmente pareja. En lugar de generar la misma cantidad de clientes o ventas en todas las provincias, el notebook intenta reflejar una distribución más realista.

## 4. Creación de `dim_geografia_ar.csv`

Se crea una tabla llamada `DimGeografia`. Cada fila representa una combinación de provincia y ciudad, con datos como:

- `GeografiaID`.
- Región.
- Provincia.
- Ciudad.
- Zona, AMBA o Interior.
- Peso de facturación.

## Por qué se hizo

Esta tabla sirve como dimensión geográfica del modelo. Una dimensión es una tabla que describe una característica importante del negocio.

En este caso, permite responder preguntas como:

- ¿Dónde están los clientes?
- ¿Qué regiones venden más?
- ¿AMBA se comporta distinto al Interior?
- ¿Qué ciudades concentran más operación?

## 5. Creación de `dim_sucursales_ar.csv`

El notebook genera 50 sucursales ficticias. Cada sucursal tiene:

- Identificador.
- Nombre.
- Tipo de sucursal.
- Ciudad y provincia.
- Región.
- Metros cuadrados.
- Cantidad de empleados.
- Fecha de apertura.
- Indicador de si está activa.

Los tipos incluyen tienda grande, tienda chica, dark store y centro de distribución.

## Por qué se hizo

Como el proyecto es omnicanal, no solo interesa el canal online. También se necesita representar la operación física.

Las sucursales permiten analizar ventas presenciales, retiros en punto de venta y diferencias entre formatos de tienda.

## Concepto clave: dark store

Una dark store es un local preparado para armar pedidos online, no necesariamente para atención tradicional al público. Es común en operaciones de e-commerce y entregas rápidas.

## 6. Creación de `dim_canal_ar.csv`

El notebook define cuatro canales:

- Tienda física.
- Web propia.
- App móvil.
- Marketplace.

También agrega si el canal es online o no, y un peso de facturación esperado.

## Por qué se hizo

Un proyecto omnicanal necesita comparar canales. No es lo mismo una venta en tienda física que una venta por marketplace.

Esta tabla permite responder:

- ¿Qué porcentaje de ventas viene de canales online?
- ¿Qué canal tiene más participación?
- ¿La app se comporta distinto a la web?
- ¿El marketplace domina la facturación?

## 7. Creación de `dim_clientes_ar.csv`

Se generan 10.000 clientes ficticios con:

- Nombre.
- Email.
- Teléfono.
- Provincia, ciudad, región y zona.
- Nivel socioeconómico.
- Rango de edad.
- Género.
- Canal preferido.
- Fecha de alta.

La distribución se calibra con pesos de CACE 2025 para que no sea completamente arbitraria.

## Por qué se hizo

Los clientes son una dimensión central en cualquier análisis comercial. Permiten segmentar el negocio.

Con esta tabla se pueden analizar patrones como:

- Qué regiones tienen más clientes.
- Qué rangos de edad compran más.
- Si ciertos perfiles prefieren canales online.
- Cómo se comportan distintos niveles socioeconómicos.

## Concepto clave: segmentación

Segmentar es dividir clientes o ventas en grupos para entender mejor su comportamiento. Por ejemplo, comparar clientes de AMBA contra clientes del Interior.

## 8. Creación de `fact_ventas_base_ar.csv`

El notebook genera 150.000 transacciones base. Cada venta incluye:

- Cliente.
- Canal.
- Sucursal, si corresponde.
- Fecha.
- Año, mes y trimestre.
- Medio de pago.
- Cantidad de cuotas.
- Tipo de entrega.
- Plazo de entrega.
- Evento comercial.

Algunas columnas quedan vacías, como precio, costo, producto y tiempo. El propio notebook aclara que esas columnas se completarán más adelante en el ETL con Olist y Superstore.

## Por qué se hizo

Esta tabla representa la base de hechos de ventas argentinas. Una tabla de hechos guarda eventos medibles del negocio, como una venta.

Se llama "base" porque todavía no está completa: tiene la estructura comercial argentina, pero luego debe integrarse con productos, precios y montos.

## Concepto clave: tabla de hechos

Una tabla de hechos registra eventos. En retail, una fila puede representar una venta, un ítem vendido, una entrega o un pago.

Las tablas de hechos suelen conectarse con dimensiones como cliente, producto, fecha, canal o geografía.

## 9. Incorporación de medios de pago, cuotas y logística

El notebook usa probabilidades para asignar:

- Tarjeta de crédito.
- Billetera electrónica.
- Débito online.
- Transferencia bancaria.
- Efectivo en redes de pago.
- Tipos de entrega.
- Plazos de entrega.

También distingue AMBA e Interior para simular que los tiempos de entrega no son iguales en todas las zonas.

## Por qué se hizo

Estos campos permiten analizar la operación desde una mirada comercial y logística.

Por ejemplo:

- ¿Qué medio de pago se usa más?
- ¿Cuántas ventas se hacen en cuotas?
- ¿Qué proporción se entrega a domicilio?
- ¿Los plazos son mejores en AMBA que en el Interior?

## 10. Incorporación de eventos comerciales

El notebook detecta fechas de eventos como:

- Hot Sale.
- CyberMonday.
- Día del Padre.
- Día de la Madre.
- Navidad.
- Vuelta al Cole.

## Por qué se hizo

En retail, las ventas no se distribuyen igual durante todo el año. Hay eventos que concentran más demanda.

Incluir eventos comerciales permite analizar si ciertas fechas afectan ventas, canales, medios de pago o logística.

## 11. Creación de `fact_precios_comp.csv`

El notebook crea una tabla de precios de competencia por categoría, año y mes. Incluye:

- Precio de lista propio.
- Precio web con descuento.
- Precio de la competencia.
- Porcentaje de descuento.
- `price_index`.
- Canal online asociado.

## Por qué se hizo

Esta tabla sirve para analizar posicionamiento de precios. El `price_index` compara el precio propio contra el precio de la competencia.

Si el índice es mayor a 1, significa que el precio propio es más alto que el de la competencia. Si es menor a 1, el precio propio es más barato.

## Concepto clave: price index

El `price_index` es una medida comparativa:

```text
price_index = precio propio / precio competencia
```

Ejemplo:

- `1.10` significa que somos 10% más caros.
- `0.90` significa que somos 10% más baratos.
- `1.00` significa que estamos igual que la competencia.

## Resultado del notebook

El notebook genera seis archivos:

- `dim_geografia_ar.csv`
- `dim_sucursales_ar.csv`
- `dim_canal_ar.csv`
- `dim_clientes_ar.csv`
- `fact_ventas_base_ar.csv`
- `fact_precios_comp.csv`

Estos archivos conforman una capa sintética argentina para enriquecer el modelo analítico.

## Carpeta de salida

Los archivos generados se guardan en:

```text
datos/03_sinteticos
```

El notebook usa la ruta relativa `../datos/03_sinteticos` desde la carpeta `notebooks/`.

## Cómo se conecta con el resto del proyecto

Este notebook construye las piezas argentinas que luego pueden combinarse con:

- Olist, para datos transaccionales de e-commerce.
- Superstore, para márgenes y descuentos.
- CACE, para benchmarks del comercio electrónico argentino.
- IPC y tipo de cambio, para contexto económico.

## Resumen en una frase

El notebook `01_creador_datos_sinteticos.ipynb` se hizo para crear una base argentina realista, ficticia y reproducible que permita analizar ventas, clientes, canales, logística y precios en un modelo omnicanal.

"""
Genera el diccionario de datos en Excel para el proyecto RetailIQ360.
Salida: extras/diccionario_datos_RetailIQ360.xlsx
"""

import openpyxl
from openpyxl.styles import (
    Font, Fill, PatternFill, Alignment, Border, Side, GradientFill
)
from openpyxl.utils import get_column_letter
from openpyxl.styles.numbers import FORMAT_TEXT
import os

# ---------------------------------------------------------------------------
# 1. DATOS DEL DICCIONARIO
# ---------------------------------------------------------------------------

# Colores
C_HEADER_DARK   = "1F2D3D"   # Azul muy oscuro — encabezados
C_HEADER_DIM    = "1A5276"   # Azul oscuro — dimensiones
C_HEADER_FACT   = "7B241C"   # Rojo oscuro — hechos
C_HEADER_CACE   = "7D6608"   # Ámbar oscuro — CACE
C_HEADER_REL    = "145A32"   # Verde oscuro — relaciones
C_HEADER_VER    = "4A235A"   # Púrpura — verificaciones
C_SUBHEADER     = "2C3E50"   # Azul grisáceo — subencabezados
C_LIGHT_DIM     = "D6EAF8"   # Azul claro — filas dim
C_LIGHT_FACT    = "FADBD8"   # Rojo claro — filas fact
C_LIGHT_CACE    = "FEF9E7"   # Amarillo muy claro — filas CACE
C_LIGHT_ALT     = "F2F3F4"   # Gris claro — filas alternas
C_WHITE         = "FFFFFF"
C_PK            = "F9E79F"   # Amarillo dorado — PK
C_FK            = "AED6F1"   # Azul claro — FK
C_CALC          = "A9DFBF"   # Verde claro — columna calculada

# ---------------------------------------------------------------------------
# Definición completa de tablas
# ---------------------------------------------------------------------------

TABLAS = [
    # ---- DIMENSIONES -------------------------------------------------------
    {
        "nombre": "dim_geografia_ar",
        "categoria": "Dimensión",
        "subcategoria": "AR Sintético",
        "archivo": "001_dim_geografia_ar.csv",
        "carpeta": "datos/03_sinteticos",
        "filas": 67,
        "descripcion": "Jerarquía geográfica argentina: región, provincia, ciudad y zona (AMBA/Interior). Pesos de facturación calibrados con CACE.",
        "color_cat": "DIM",
        "columnas": [
            ("GeografiaID",         "Entero",   "PK",  None,               None,               "Clave primaria única de la localidad"),
            ("region",              "Texto",    "",    None,               None,               "Región macro: AMBA, Centro, NOA, NEA, Patagonia, Cuyo"),
            ("provincia",           "Texto",    "",    None,               None,               "Nombre completo de la provincia"),
            ("ciudad",              "Texto",    "",    None,               None,               "Ciudad o localidad"),
            ("zona",                "Texto",    "",    None,               None,               "AMBA o Interior"),
            ("peso_facturacion",    "Decimal",  "",    None,               None,               "Peso relativo de facturación calibrado con CACE (suma 1.0 por región)"),
        ],
    },
    {
        "nombre": "dim_canal_ar",
        "categoria": "Dimensión",
        "subcategoria": "AR Sintético",
        "archivo": "003_dim_canal_ar.csv",
        "carpeta": "datos/03_sinteticos",
        "filas": 4,
        "descripcion": "Canales de venta: Tienda física, Web propia, App móvil y Marketplace. Pesos calibrados con CACE 2025.",
        "color_cat": "DIM",
        "columnas": [
            ("CanalID",             "Entero",   "PK",  None,               None,               "Clave primaria (1 a 4)"),
            ("nombre",              "Texto",    "",    None,               None,               "Nombre del canal: Tienda física, Web propia, App móvil, Marketplace"),
            ("tipo",                "Texto",    "",    None,               None,               "Físico, Online o Marketplace"),
            ("plataforma",          "Texto",    "",    None,               None,               "POS físico, Sitio web, App iOS/Android, MercadoLibre"),
            ("flag_online",         "Entero",   "",    None,               None,               "0 = presencial, 1 = online"),
            ("peso_facturacion",    "Decimal",  "",    None,               None,               "Peso calibrado CACE: Físico 8%, Web 25%, App 20%, Marketplace 47%"),
        ],
    },
    {
        "nombre": "dim_sucursales_ar",
        "categoria": "Dimensión",
        "subcategoria": "AR Sintético",
        "archivo": "002_dim_sucursales_ar.csv",
        "carpeta": "datos/03_sinteticos",
        "filas": 50,
        "descripcion": "Red de 50 sucursales físicas de RetailIQ Argentina. Incluye FK a dim_geografia_ar.",
        "color_cat": "DIM",
        "columnas": [
            ("SucursalID",      "Entero",   "PK",  None,               None,               "Clave primaria única de la sucursal"),
            ("nombre",          "Texto",    "",    None,               None,               "Nombre de la sucursal (ej: RetailIQ Avellaneda 1)"),
            ("tipo",            "Texto",    "",    None,               None,               "Tienda grande, Tienda chica o Dark store"),
            ("GeografiaID",     "Entero",   "FK",  "dim_geografia_ar", "GeografiaID",      "FK → dim_geografia_ar. Ubicación geográfica de la sucursal"),
            ("provincia",       "Texto",    "",    None,               None,               "Provincia donde está la sucursal (desnormalizado para filtros rápidos)"),
            ("ciudad",          "Texto",    "",    None,               None,               "Ciudad donde está la sucursal (desnormalizado)"),
            ("region",          "Texto",    "",    None,               None,               "Región macro (desnormalizado)"),
            ("m2_ventas",       "Entero",   "",    None,               None,               "Metros cuadrados del área de ventas"),
            ("empleados",       "Entero",   "",    None,               None,               "Cantidad de empleados"),
            ("fecha_apertura",  "Fecha",    "",    None,               None,               "Fecha de apertura de la sucursal"),
            ("flag_activa",     "Entero",   "",    None,               None,               "1 = activa, 0 = cerrada"),
        ],
    },
    {
        "nombre": "dim_clientes_ar",
        "categoria": "Dimensión",
        "subcategoria": "AR Sintético",
        "archivo": "004_dim_clientes_ar.csv",
        "carpeta": "datos/03_sinteticos",
        "filas": 10000,
        "descripcion": "10 000 clientes sintéticos generados con Faker. Perfil sociodemográfico calibrado con CACE. NO tiene FK a dim_geografia_ar.",
        "color_cat": "DIM",
        "columnas": [
            ("ClienteID",       "Entero",   "PK",  None,  None,  "Clave primaria única del cliente"),
            ("nombre",          "Texto",    "",    None,  None,  "Nombre completo (generado con Faker)"),
            ("email",           "Texto",    "",    None,  None,  "Email del cliente (único)"),
            ("telefono",        "Texto",    "",    None,  None,  "Teléfono con formato argentino (+54)"),
            ("provincia",       "Texto",    "",    None,  None,  "Provincia de residencia (texto libre, sin FK)"),
            ("ciudad",          "Texto",    "",    None,  None,  "Ciudad de residencia (texto libre, sin FK)"),
            ("region",          "Texto",    "",    None,  None,  "Región macro (texto libre, sin FK)"),
            ("zona",            "Texto",    "",    None,  None,  "AMBA o Interior (texto libre, sin FK)"),
            ("nse",             "Texto",    "",    None,  None,  "Nivel socioeconómico: ABC1, C2, C3, D (calibrado CACE)"),
            ("rango_edad",      "Texto",    "",    None,  None,  "Segmento etario: 18-20, 21-29, 30-34, 35-44, 45-59, 60+"),
            ("genero",          "Texto",    "",    None,  None,  "M o F (distribución 50/50 calibrada CACE)"),
            ("canal_preferido", "Texto",    "",    None,  None,  "Canal de compra preferido"),
            ("segmento_rfm",    "Texto",    "",    None,  None,  "Segmento RFM (puede estar vacío)"),
            ("fecha_alta",      "Fecha",    "",    None,  None,  "Fecha de registro del cliente"),
        ],
    },
    {
        "nombre": "dim_inflacion_ipc",
        "categoria": "Dimensión",
        "subcategoria": "Olist Procesado",
        "archivo": "dim_inflacion_ipc.csv",
        "carpeta": "datos/04_procesados",
        "filas": 111,
        "descripcion": "Serie mensual de IPC Argentina (2017-2026) por rubro. Fuente: INDEC. Se vincula con fact_ventas mediante columna calculada anio_mes.",
        "color_cat": "DIM",
        "columnas": [
            ("fecha",                       "Fecha",    "",     None,  None,  "Primer día del mes (ej: 2017-01-01)"),
            ("ipc_nivel_general",           "Decimal",  "",     None,  None,  "Variación mensual IPC general en porcentaje"),
            ("ipc_alimentos_bebidas",       "Decimal",  "",     None,  None,  "Variación mensual IPC alimentos y bebidas"),
            ("ipc_indumentaria_calzado",    "Decimal",  "",     None,  None,  "Variación mensual IPC indumentaria y calzado"),
            ("ipc_equipamiento_hogar",      "Decimal",  "",     None,  None,  "Variación mensual IPC equipamiento del hogar"),
            ("ipc_transporte",              "Decimal",  "",     None,  None,  "Variación mensual IPC transporte"),
            ("ipc_comunicacion",            "Decimal",  "",     None,  None,  "Variación mensual IPC comunicación"),
            ("anio",                        "Entero",   "",     None,  None,  "Año (2017 a 2026)"),
            ("mes",                         "Entero",   "",     None,  None,  "Mes (1 a 12)"),
            ("anio_mes",                    "Texto",    "CALC", None,  None,  "Columna calculada en Power BI: FORMAT([anio],\"0000\") & \"-\" & FORMAT([mes],\"00\"). Usada como PK compuesta para relación con fact_ventas"),
        ],
    },
    # ---- HECHOS ------------------------------------------------------------
    {
        "nombre": "fact_ventas",
        "categoria": "Tabla de hechos",
        "subcategoria": "Olist Procesado",
        "archivo": "fact_ventas.csv",
        "carpeta": "datos/04_procesados",
        "filas": 110197,
        "descripcion": "Transacciones reales de Olist Brasil (2016-2018) procesadas: conversión BRL→ARS y deflación por IPC. Es el resultado del ETL sobre los 9 archivos raw de Olist.",
        "color_cat": "FACT",
        "columnas": [
            ("order_id",            "Texto",    "",     None,               None,               "ID de la orden original de Olist (puede repetirse si tiene varios ítems)"),
            ("product_id",          "Texto",    "",     None,               None,               "ID del producto original de Olist"),
            ("seller_id",           "Texto",    "",     None,               None,               "ID del vendedor original de Olist"),
            ("fecha",               "Fecha",    "",     None,               None,               "Fecha de la transacción"),
            ("anio",                "Entero",   "",     None,               None,               "Año (2016 a 2018)"),
            ("mes",                 "Entero",   "",     None,               None,               "Mes (1 a 12)"),
            ("trimestre",           "Entero",   "",     None,               None,               "Trimestre (1 a 4)"),
            ("category_en",         "Texto",    "",     None,               None,               "Categoría del producto en inglés (72 categorías)"),
            ("price_brl",           "Decimal",  "",     None,               None,               "Precio unitario en Reales brasileños (BRL)"),
            ("freight_brl",         "Decimal",  "",     None,               None,               "Costo de flete en BRL"),
            ("ars_por_usd",         "Decimal",  "",     None,               None,               "Tipo de cambio ARS/USD del día de la transacción"),
            ("tipo_cambio",         "Decimal",  "",     None,               None,               "Factor de conversión BRL→ARS (ars_por_usd ÷ 3.3)"),
            ("price_ars",           "Decimal",  "",     None,               None,               "Precio en ARS nominal (price_brl × tipo_cambio)"),
            ("freight_ars",         "Decimal",  "",     None,               None,               "Flete en ARS nominal"),
            ("ipc_nivel_general",   "Decimal",  "",     None,               None,               "Variación IPC del mes (copiado de dim_inflacion_ipc)"),
            ("indice_ipc_acum",     "Decimal",  "",     None,               None,               "Índice IPC acumulado desde dic-2016 (base = 1.0)"),
            ("price_ars_real",      "Decimal",  "",     None,               None,               "Precio en ARS constantes de dic-2016 (price_ars ÷ indice_ipc_acum)"),
            ("tiene_ipc",           "Booleano", "",     None,               None,               "True si tiene cobertura IPC; False para sep-dic 2016 (267 registros)"),
            ("anio_mes",            "Texto",    "CALC", "dim_inflacion_ipc","anio_mes",         "Columna calculada en Power BI: FORMAT([anio],\"0000\") & \"-\" & FORMAT([mes],\"00\"). FK → dim_inflacion_ipc"),
        ],
    },
    {
        "nombre": "fact_ventas_base_ar",
        "categoria": "Tabla de hechos",
        "subcategoria": "AR Sintético",
        "archivo": "005_fact_ventas_base_ar.csv",
        "carpeta": "datos/03_sinteticos",
        "filas": 150000,
        "descripcion": "150 000 transacciones sintéticas argentinas generadas con Faker y calibradas con benchmarks CACE 2025. Eje central de la Constelación AR.",
        "color_cat": "FACT",
        "columnas": [
            ("VentaID",             "Entero",   "PK",  None,               None,               "Clave primaria única de la venta"),
            ("ClienteID",           "Entero",   "FK",  "dim_clientes_ar",  "ClienteID",        "FK → dim_clientes_ar"),
            ("CanalID",             "Entero",   "FK",  "dim_canal_ar",     "CanalID",          "FK → dim_canal_ar (1=Tienda, 2=Web, 3=App, 4=Marketplace)"),
            ("SucursalID",          "Entero",   "FK",  "dim_sucursales_ar","SucursalID",       "FK → dim_sucursales_ar. Nulo si la venta es online pura"),
            ("fecha",               "Fecha",    "",    None,               None,               "Fecha de la transacción"),
            ("anio",                "Entero",   "",    None,               None,               "Año"),
            ("mes",                 "Entero",   "",    None,               None,               "Mes"),
            ("trimestre",           "Entero",   "",    None,               None,               "Trimestre"),
            ("medio_pago",          "Texto",    "",    None,               None,               "Medio de pago (calibrado CACE): tarjeta crédito, débito, transferencia, efectivo"),
            ("nro_cuotas",          "Entero",   "",    None,               None,               "Número de cuotas: 1, 3, 6, 10 o 15 (calibrado CACE)"),
            ("tipo_entrega",        "Texto",    "",    None,               None,               "Tipo de entrega: envio_domicilio, retiro_punto_venta, pickup_point, locker"),
            ("plazo_entrega",       "Texto",    "",    None,               None,               "Plazo de entrega: same_day, 24hs, 48hs, en_semana, 15_dias, mes_mas"),
            ("evento_comercial",    "Texto",    "",    None,               None,               "Evento comercial: Hot Sale, Cyber Monday, etc. (puede ser nulo)"),
            ("precio_venta_ars",    "Decimal",  "",    None,               None,               "Precio de venta al público en ARS"),
            ("costo_unitario_ars",  "Decimal",  "",    None,               None,               "Costo del producto en ARS"),
            ("cantidad",            "Entero",   "",    None,               None,               "Unidades vendidas"),
            ("ProductoID",          "Entero",   "",    None,               None,               "FK potencial a dimensión de producto (puede no estar cargada en Power BI)"),
            ("TiempoID",            "Entero",   "",    None,               None,               "FK potencial a dimensión de tiempo (puede no estar cargada en Power BI)"),
        ],
    },
    {
        "nombre": "fact_precios_comp",
        "categoria": "Tabla de hechos",
        "subcategoria": "AR Sintético",
        "archivo": "006_fact_precios_comp.csv",
        "carpeta": "datos/03_sinteticos",
        "filas": 360,
        "descripcion": "Precios relevados mensualmente por categoría (30 categorías × 12 meses). Incluye precio propio y precio de competencia para calcular price index.",
        "color_cat": "FACT",
        "columnas": [
            ("PrecioID",            "Entero",   "PK",  None,           None,       "Clave primaria del registro de precio"),
            ("categoria",           "Texto",    "",    None,           None,       "Categoría de producto relevada"),
            ("anio",                "Entero",   "",    None,           None,       "Año del relevamiento"),
            ("mes",                 "Entero",   "",    None,           None,       "Mes del relevamiento"),
            ("fecha_relevamiento",  "Fecha",    "",    None,           None,       "Fecha del relevamiento (día 15 de cada mes)"),
            ("precio_lista_ars",    "Decimal",  "",    None,           None,       "Precio de lista propio en ARS"),
            ("precio_web_ars",      "Decimal",  "",    None,           None,       "Precio online propio en ARS (usualmente < precio_lista)"),
            ("precio_competencia",  "Decimal",  "",    None,           None,       "Precio promedio de competencia en ARS"),
            ("descuento_pct",       "Decimal",  "",    None,           None,       "Descuento aplicado (entre 0 y 1)"),
            ("price_index",         "Decimal",  "",    None,           None,       "Índice precio propio / precio competencia (< 1 = más barato que competencia)"),
            ("CanalID",             "Entero",   "FK",  "dim_canal_ar", "CanalID",  "FK → dim_canal_ar. Canal donde aplica el precio relevado"),
        ],
    },
    # ---- CACE BENCHMARKS ---------------------------------------------------
    {
        "nombre": "cace_01_kpis_macro",
        "categoria": "Benchmark CACE",
        "subcategoria": "Macro",
        "archivo": "cace_01_kpis_macro.csv",
        "carpeta": "datos/02_cace_benchmarks",
        "filas": 50,
        "descripcion": "KPIs macro del eCommerce argentino 2021-2025: facturación total, órdenes, unidades, ticket promedio, tasa de conversión, inflación y crecimiento YoY.",
        "color_cat": "CACE",
        "columnas": [
            ("indicador",       "Texto",    "",    None, None, "Nombre del indicador: facturacion_total, ordenes_totales, ticket_promedio, etc."),
            ("anio",            "Entero",   "",    None, None, "Año del indicador (2021 a 2025)"),
            ("periodo",         "Texto",    "",    None, None, "Anual, H1 (primer semestre) o MID (mitad de año)"),
            ("valor",           "Decimal",  "",    None, None, "Valor numérico del indicador"),
            ("unidad",          "Texto",    "",    None, None, "Unidad del valor: ARS, unidades, porcentaje, etc."),
            ("fuente_pagina",   "Texto",    "",    None, None, "Página del informe CACE de donde proviene el dato"),
            ("uso_proyecto",    "Texto",    "",    None, None, "Clasificación: benchmark, kpi_referencia, contexto o sintetico"),
        ],
    },
    {
        "nombre": "cace_02_categorias_rubros",
        "categoria": "Benchmark CACE",
        "subcategoria": "Categorías",
        "archivo": "cace_02_categorias_rubros.csv",
        "carpeta": "datos/02_cace_benchmarks",
        "filas": 14,
        "descripcion": "Facturación del eCommerce argentino por categoría de producto (2021-2025). Incluye participación porcentual y rankings.",
        "color_cat": "CACE",
        "columnas": [
            ("categoria_rubro",             "Texto",    "", None, None, "Nombre oficial de la categoría según CACE"),
            ("categoria_simplificada",      "Texto",    "", None, None, "Nombre corto para joins con datos propios"),
            ("facturacion_2021_mARS",       "Decimal",  "", None, None, "Facturación 2021 en millones de ARS"),
            ("facturacion_2022_mARS",       "Decimal",  "", None, None, "Facturación 2022 en millones de ARS"),
            ("facturacion_2023_mARS",       "Decimal",  "", None, None, "Facturación 2023 en millones de ARS"),
            ("facturacion_2024_mARS",       "Decimal",  "", None, None, "Facturación 2024 en millones de ARS"),
            ("facturacion_2025_mARS",       "Decimal",  "", None, None, "Facturación 2025 en millones de ARS"),
            ("participacion_2025_pct",      "Decimal",  "", None, None, "Participación porcentual en la facturación total 2025 (suma ≈ 100)"),
            ("crecimiento_2024_2025_pct",   "Decimal",  "", None, None, "Crecimiento porcentual 2024 vs 2025"),
            ("ranking_unidades_2025",       "Entero",   "", None, None, "Ranking por unidades vendidas en 2025"),
            ("ranking_facturacion_2025",    "Entero",   "", None, None, "Ranking por facturación en 2025"),
            ("fuente_pagina",               "Texto",    "", None, None, "Página del informe CACE"),
            ("uso_proyecto",                "Texto",    "", None, None, "Clasificación del uso en el proyecto"),
        ],
    },
    {
        "nombre": "cace_03a_conversion_por_categoria",
        "categoria": "Benchmark CACE",
        "subcategoria": "Conversión",
        "archivo": "cace_03a_conversion_por_categoria.csv",
        "carpeta": "datos/02_cace_benchmarks",
        "filas": 5,
        "descripcion": "Tasa de conversión (%) por categoría para H1 2024 y H1 2025. Incluye variación en puntos porcentuales.",
        "color_cat": "CACE",
        "columnas": [
            ("categoria",               "Texto",    "", None, None, "Categoría de producto (incluye fila Total promedio)"),
            ("tasa_conversion_H1_2024", "Decimal",  "", None, None, "Tasa de conversión H1 2024 en porcentaje"),
            ("tasa_conversion_H1_2025", "Decimal",  "", None, None, "Tasa de conversión H1 2025 en porcentaje"),
            ("variacion_pp",            "Decimal",  "", None, None, "Variación en puntos porcentuales (H1 2025 - H1 2024)"),
            ("fuente_pagina",           "Texto",    "", None, None, "Página del informe CACE"),
            ("uso_proyecto",            "Texto",    "", None, None, "Clasificación del uso en el proyecto"),
        ],
    },
    {
        "nombre": "cace_03b_ranking_demanda",
        "categoria": "Benchmark CACE",
        "subcategoria": "Categorías",
        "archivo": "cace_03b_ranking_demanda.csv",
        "carpeta": "datos/02_cace_benchmarks",
        "filas": 10,
        "descripcion": "Ranking de las 10 categorías más demandadas en 2023, 2024 y 2025 por unidades vendidas.",
        "color_cat": "CACE",
        "columnas": [
            ("ranking_2025",    "Entero",   "", None, None, "Posición en el ranking 2025 (1 = mayor demanda)"),
            ("categoria",       "Texto",    "", None, None, "Nombre de la categoría"),
            ("ranking_2024",    "Entero",   "", None, None, "Posición en el ranking 2024"),
            ("ranking_2023",    "Entero",   "", None, None, "Posición en el ranking 2023"),
            ("fuente_pagina",   "Texto",    "", None, None, "Página del informe CACE"),
            ("uso_proyecto",    "Texto",    "", None, None, "Clasificación del uso en el proyecto"),
        ],
    },
    {
        "nombre": "cace_04a_medios_pago_oferta",
        "categoria": "Benchmark CACE",
        "subcategoria": "Medios de pago",
        "archivo": "cace_04a_medios_pago_oferta.csv",
        "carpeta": "datos/02_cace_benchmarks",
        "filas": 8,
        "descripcion": "Distribución porcentual de medios de pago en eCommerce argentino (2022-2025). Para comparar con fact_ventas_base_ar.medio_pago.",
        "color_cat": "CACE",
        "columnas": [
            ("medio_pago",      "Texto",    "", None, None, "Medio de pago: tarjeta crédito, débito, transferencia, efectivo, etc."),
            ("tipo",            "Texto",    "", None, None, "Categoría: credito, debito, transferencia, efectivo"),
            ("MID_2022_pct",    "Decimal",  "", None, None, "Porcentaje de uso en mitad de 2022"),
            ("MID_2023_pct",    "Decimal",  "", None, None, "Porcentaje de uso en mitad de 2023"),
            ("MID_2024_pct",    "Decimal",  "", None, None, "Porcentaje de uso en mitad de 2024"),
            ("Anual_2024_pct",  "Decimal",  "", None, None, "Porcentaje de uso anual 2024"),
            ("MID_2025_pct",    "Decimal",  "", None, None, "Porcentaje de uso en mitad de 2025"),
            ("Anual_2025_pct",  "Decimal",  "", None, None, "Porcentaje de uso anual 2025 (suma ≈ 100)"),
            ("fuente_pagina",   "Texto",    "", None, None, "Página del informe CACE"),
            ("uso_proyecto",    "Texto",    "", None, None, "Clasificación del uso en el proyecto"),
        ],
    },
    {
        "nombre": "cace_04b_financiamiento_cuotas",
        "categoria": "Benchmark CACE",
        "subcategoria": "Medios de pago",
        "archivo": "cace_04b_financiamiento_cuotas.csv",
        "carpeta": "datos/02_cace_benchmarks",
        "filas": 5,
        "descripcion": "Distribución de ventas por cantidad de cuotas en 2024 y 2025. Para comparar con fact_ventas_base_ar.nro_cuotas.",
        "color_cat": "CACE",
        "columnas": [
            ("plazo_cuotas",        "Entero",   "", None, None, "Cantidad de cuotas: 1, 3, 6, 10 o 15"),
            ("label",               "Texto",    "", None, None, "Etiqueta descriptiva: Contado, 3 cuotas, etc."),
            ("pct_ventas_2024",     "Decimal",  "", None, None, "Porcentaje de ventas en ese plazo en 2024 (suma = 100)"),
            ("pct_ventas_2025",     "Decimal",  "", None, None, "Porcentaje de ventas en ese plazo en 2025 (suma = 100)"),
            ("fuente_pagina",       "Texto",    "", None, None, "Página del informe CACE"),
            ("uso_proyecto",        "Texto",    "", None, None, "Clasificación del uso en el proyecto"),
        ],
    },
    {
        "nombre": "cace_05a_logistica_tipo_entrega",
        "categoria": "Benchmark CACE",
        "subcategoria": "Logística",
        "archivo": "cace_05a_logistica_tipo_entrega.csv",
        "carpeta": "datos/02_cace_benchmarks",
        "filas": 5,
        "descripcion": "Distribución de tipos de entrega en eCommerce argentino (2023-2025). Para comparar con fact_ventas_base_ar.tipo_entrega.",
        "color_cat": "CACE",
        "columnas": [
            ("tipo_entrega",    "Texto",    "", None, None, "Tipo de entrega: envio_domicilio, retiro_punto_venta, pickup_point, locker"),
            ("pct_2023",        "Decimal",  "", None, None, "Porcentaje de uso en 2023"),
            ("pct_2024_anual",  "Decimal",  "", None, None, "Porcentaje de uso anual 2024"),
            ("pct_2025_anual",  "Decimal",  "", None, None, "Porcentaje de uso anual 2025 (suma ≈ 100)"),
            ("pct_2025_H1",     "Decimal",  "", None, None, "Porcentaje de uso en H1 2025"),
            ("fuente_pagina",   "Texto",    "", None, None, "Página del informe CACE"),
            ("uso_proyecto",    "Texto",    "", None, None, "Clasificación del uso en el proyecto"),
        ],
    },
    {
        "nombre": "cace_05b_plazos_entrega",
        "categoria": "Benchmark CACE",
        "subcategoria": "Logística",
        "archivo": "cace_05b_plazos_entrega.csv",
        "carpeta": "datos/02_cace_benchmarks",
        "filas": 6,
        "descripcion": "Distribución de plazos de entrega (2023-2025) con apertura AMBA vs Interior. Para comparar con fact_ventas_base_ar.plazo_entrega.",
        "color_cat": "CACE",
        "columnas": [
            ("plazo_entrega",       "Texto",    "", None, None, "Plazo de entrega: same_day, 24hs, 48hs, semana, 15dias, mes_mas"),
            ("label_corto",         "Texto",    "", None, None, "Etiqueta corta para visualizaciones"),
            ("pct_2023",            "Decimal",  "", None, None, "Porcentaje de uso en 2023"),
            ("pct_2024",            "Decimal",  "", None, None, "Porcentaje de uso en 2024"),
            ("pct_2025_anual",      "Decimal",  "", None, None, "Porcentaje de uso anual 2025 (suma = 100)"),
            ("pct_AMBA_2025",       "Decimal",  "", None, None, "Porcentaje AMBA 2025 (suma = 100 dentro de zona)"),
            ("pct_interior_2025",   "Decimal",  "", None, None, "Porcentaje Interior 2025 (suma = 100 dentro de zona)"),
            ("fuente_pagina",       "Texto",    "", None, None, "Página del informe CACE"),
            ("uso_proyecto",        "Texto",    "", None, None, "Clasificación del uso en el proyecto"),
        ],
    },
    {
        "nombre": "cace_06a_distribucion_regional",
        "categoria": "Benchmark CACE",
        "subcategoria": "Geografía",
        "archivo": "cace_06a_distribucion_regional.csv",
        "carpeta": "datos/02_cace_benchmarks",
        "filas": 7,
        "descripcion": "Participación regional en la facturación del eCommerce argentino (2024-2025). Para comparar con la distribución geográfica de ventas propias.",
        "color_cat": "CACE",
        "columnas": [
            ("region",                  "Texto",    "", None, None, "Región: GBA, NOA, NEA, Cuyo, Centro, Patagonia, AMBA interior"),
            ("provincias",              "Texto",    "", None, None, "Lista de provincias que componen la región"),
            ("pct_facturacion_2024",    "Decimal",  "", None, None, "Porcentaje de la facturación nacional en 2024"),
            ("pct_facturacion_2025",    "Decimal",  "", None, None, "Porcentaje de la facturación nacional en 2025 (suma = 100)"),
            ("variacion_pp",            "Decimal",  "", None, None, "Variación en puntos porcentuales (2025 - 2024)"),
            ("zona_simplificada",       "Texto",    "", None, None, "AMBA o Interior (para comparación con dim_geografia_ar.zona)"),
            ("fuente_pagina",           "Texto",    "", None, None, "Página del informe CACE"),
            ("uso_proyecto",            "Texto",    "", None, None, "Clasificación del uso en el proyecto"),
        ],
    },
    {
        "nombre": "cace_06b_perfil_comprador",
        "categoria": "Benchmark CACE",
        "subcategoria": "Perfil cliente",
        "archivo": "cace_06b_perfil_comprador.csv",
        "carpeta": "datos/02_cace_benchmarks",
        "filas": 13,
        "descripcion": "Perfil sociodemográfico del comprador online argentino 2025: género, NSE y rango etario. Para comparar con dim_clientes_ar.",
        "color_cat": "CACE",
        "columnas": [
            ("variable",        "Texto",    "", None, None, "Dimensión demográfica: genero, nse, edad"),
            ("segmento",        "Texto",    "", None, None, "Valor del segmento: M, F, ABC1, C2, C3, D, 18-24, 25-34, etc."),
            ("pct_2025",        "Decimal",  "", None, None, "Porcentaje de compradores en ese segmento (suma = 100 dentro de cada variable)"),
            ("fuente_pagina",   "Texto",    "", None, None, "Página del informe CACE"),
            ("uso_proyecto",    "Texto",    "", None, None, "Clasificación del uso en el proyecto"),
        ],
    },
    {
        "nombre": "cace_07_canal_online_por_categoria",
        "categoria": "Benchmark CACE",
        "subcategoria": "Canal",
        "archivo": "cace_07_canal_online_por_categoria.csv",
        "carpeta": "datos/02_cace_benchmarks",
        "filas": 9,
        "descripcion": "Porcentaje de ventas online sobre el total, por categoría, para H1 2024 y H1 2025. Para comparar con el mix de canales propio.",
        "color_cat": "CACE",
        "columnas": [
            ("categoria",                   "Texto",    "", None, None, "Categoría de producto (incluye fila Total empresas BM)"),
            ("pct_canal_online_H1_2024",    "Decimal",  "", None, None, "Porcentaje online H1 2024"),
            ("pct_canal_online_H1_2025",    "Decimal",  "", None, None, "Porcentaje online H1 2025"),
            ("variacion_pp",                "Decimal",  "", None, None, "Variación en puntos porcentuales (H1 2025 - H1 2024)"),
            ("fuente_pagina",               "Texto",    "", None, None, "Página del informe CACE"),
            ("uso_proyecto",                "Texto",    "", None, None, "Clasificación del uso en el proyecto"),
        ],
    },
]

RELACIONES = [
    ("dim_sucursales_ar",   "GeografiaID",  "dim_geografia_ar",     "GeografiaID",  "N:1",  "Formal",     "Configurar en Model View de Power BI"),
    ("fact_ventas_base_ar", "ClienteID",    "dim_clientes_ar",      "ClienteID",    "N:1",  "Formal",     "Configurar en Model View de Power BI"),
    ("fact_ventas_base_ar", "CanalID",      "dim_canal_ar",         "CanalID",      "N:1",  "Formal",     "Configurar en Model View de Power BI"),
    ("fact_ventas_base_ar", "SucursalID",   "dim_sucursales_ar",    "SucursalID",   "N:1",  "Formal",     "SucursalID puede ser nulo para ventas online puras"),
    ("fact_precios_comp",   "CanalID",      "dim_canal_ar",         "CanalID",      "N:1",  "Formal",     "Configurar en Model View de Power BI"),
    ("fact_ventas",         "anio_mes*",    "dim_inflacion_ipc",    "anio_mes*",    "N:1",  "Calculada",  "Crear columna calculada: FORMAT([anio],\"0000\") & \"-\" & FORMAT([mes],\"00\")"),
]

VERIFICACIONES = [
    # (tabla, nro, texto, tipo)
    ("dim_geografia_ar",    1,  "No hay GeografiaID duplicados",                                "Integridad"),
    ("dim_geografia_ar",    2,  "Los 67 registros cubren todas las provincias de Argentina",    "Negocio"),
    ("dim_geografia_ar",    3,  "peso_facturacion suma 1.0 agrupado por zona o región",         "Negocio"),
    ("dim_geografia_ar",    4,  "Sin valores nulos en GeografiaID, region, provincia, ciudad",  "Integridad"),
    ("dim_canal_ar",        1,  "Exactamente 4 filas, sin duplicados",                          "Integridad"),
    ("dim_canal_ar",        2,  "peso_facturacion suma exactamente 1.0",                        "Negocio"),
    ("dim_canal_ar",        3,  "flag_online contiene solo valores 0 y 1",                      "Formato"),
    ("dim_canal_ar",        4,  "Los 4 CanalID (1, 2, 3, 4) están en fact_ventas_base_ar",     "Integridad"),
    ("dim_sucursales_ar",   1,  "No hay SucursalID duplicados",                                 "Integridad"),
    ("dim_sucursales_ar",   2,  "Todos los GeografiaID existen en dim_geografia_ar",            "Integridad"),
    ("dim_sucursales_ar",   3,  "flag_activa contiene solo valores 0 y 1",                      "Formato"),
    ("dim_sucursales_ar",   4,  "fecha_apertura tiene formato fecha válido (sin texto ni nulos)","Formato"),
    ("dim_sucursales_ar",   5,  "m2_ventas y empleados son valores positivos",                  "Negocio"),
    ("dim_clientes_ar",     1,  "No hay ClienteID duplicados (deben ser 10.000 únicos)",        "Integridad"),
    ("dim_clientes_ar",     2,  "Todos los ClienteID de fact_ventas_base_ar existen en esta tabla","Integridad"),
    ("dim_clientes_ar",     3,  "Distribución de nse: ABC1 ~24%, C2 ~26%, C3 ~30%, D ~20%",    "Negocio"),
    ("dim_clientes_ar",     4,  "Distribución de genero: ~50% M y ~50% F",                      "Negocio"),
    ("dim_clientes_ar",     5,  "email sin duplicados",                                         "Integridad"),
    ("dim_clientes_ar",     6,  "fecha_alta tiene formato fecha válido",                        "Formato"),
    ("dim_inflacion_ipc",   1,  "No hay combinaciones (anio, mes) duplicadas",                  "Integridad"),
    ("dim_inflacion_ipc",   2,  "La serie es continua desde enero 2017 (sin huecos)",           "Integridad"),
    ("dim_inflacion_ipc",   3,  "Sin valores nulos en ipc_nivel_general",                       "Integridad"),
    ("dim_inflacion_ipc",   4,  "ipc_nivel_general está entre -5% y 30% mensual",              "Negocio"),
    ("fact_ventas",         1,  "110.197 filas exactas después de la carga",                    "Integridad"),
    ("fact_ventas",         2,  "order_id + product_id no tiene duplicados",                    "Integridad"),
    ("fact_ventas",         3,  "fecha está entre 2016-09-02 y 2018-08-29",                     "Negocio"),
    ("fact_ventas",         4,  "price_brl y price_ars son positivos (sin negativos ni ceros)",  "Negocio"),
    ("fact_ventas",         5,  "tiene_ipc es False solo para sep-dic 2016 (267 filas)",        "Negocio"),
    ("fact_ventas",         6,  "indice_ipc_acum empieza en 1.0 y es siempre creciente",        "Negocio"),
    ("fact_ventas",         7,  "price_ars_real = price_ars / indice_ipc_acum (verificar fórmula)","Negocio"),
    ("fact_ventas_base_ar", 1,  "150.000 filas exactas después de la carga",                    "Integridad"),
    ("fact_ventas_base_ar", 2,  "No hay VentaID duplicados",                                    "Integridad"),
    ("fact_ventas_base_ar", 3,  "Todos los ClienteID existen en dim_clientes_ar",               "Integridad"),
    ("fact_ventas_base_ar", 4,  "Todos los CanalID existen en dim_canal_ar (valores 1 a 4)",    "Integridad"),
    ("fact_ventas_base_ar", 5,  "Los SucursalID no nulos existen en dim_sucursales_ar",         "Integridad"),
    ("fact_ventas_base_ar", 6,  "CanalID=4 (Marketplace) representa ~47% de las filas",         "Negocio"),
    ("fact_ventas_base_ar", 7,  "precio_venta_ars y costo_unitario_ars son positivos",          "Negocio"),
    ("fact_ventas_base_ar", 8,  "nro_cuotas toma valores 1, 3, 6, 10 o 15",                     "Formato"),
    ("fact_precios_comp",   1,  "360 filas exactas (30 categorías × 12 meses)",                 "Integridad"),
    ("fact_precios_comp",   2,  "No hay PrecioID duplicados",                                    "Integridad"),
    ("fact_precios_comp",   3,  "Todos los CanalID existen en dim_canal_ar",                    "Integridad"),
    ("fact_precios_comp",   4,  "descuento_pct está entre 0 y 1",                              "Negocio"),
    ("fact_precios_comp",   5,  "price_index es positivo",                                      "Negocio"),
    ("fact_precios_comp",   6,  "precio_web_ars < precio_lista_ars en la mayoría de casos",     "Negocio"),
    ("cace_01_kpis_macro",  1,  "Sin combinaciones (indicador, anio, periodo) duplicadas",      "Integridad"),
    ("cace_01_kpis_macro",  2,  "valor no tiene nulos en los indicadores principales",          "Integridad"),
    ("cace_01_kpis_macro",  3,  "uso_proyecto distingue benchmark, kpi_referencia, contexto",   "Formato"),
    ("cace_02_categorias_rubros", 1, "participacion_2025_pct suma ~100",                        "Negocio"),
    ("cace_02_categorias_rubros", 2, "categoria_simplificada sin duplicados",                   "Integridad"),
    ("cace_03a_conversion_por_categoria", 1, "Tasas entre 0 y 10 (son porcentajes)",           "Negocio"),
    ("cace_03b_ranking_demanda", 1, "Rankings sin números repetidos dentro del mismo año",      "Integridad"),
    ("cace_03b_ranking_demanda", 2, "Exactamente 10 filas (top 10)",                            "Integridad"),
    ("cace_04a_medios_pago_oferta", 1, "Anual_2025_pct suma ~100",                             "Negocio"),
    ("cace_04b_financiamiento_cuotas", 1, "pct_ventas_2024 y pct_ventas_2025 suman 100",       "Negocio"),
    ("cace_05a_logistica_tipo_entrega", 1, "pct_2025_anual suma ~100",                         "Negocio"),
    ("cace_05b_plazos_entrega", 1, "pct_2025_anual suma 100",                                   "Negocio"),
    ("cace_05b_plazos_entrega", 2, "pct_AMBA_2025 y pct_interior_2025 suman 100 cada una",     "Negocio"),
    ("cace_06a_distribucion_regional", 1, "pct_facturacion_2025 suma 100",                     "Negocio"),
    ("cace_06b_perfil_comprador", 1, "pct_2025 suma 100 dentro de cada variable",              "Negocio"),
    ("cace_06b_perfil_comprador", 2, "Segmentos de nse y edad coinciden con dim_clientes_ar",  "Negocio"),
    ("cace_07_canal_online_por_categoria", 1, "Porcentajes entre 0 y 100",                     "Negocio"),
]

# ---------------------------------------------------------------------------
# 2. FUNCIONES AUXILIARES DE ESTILO
# ---------------------------------------------------------------------------

def make_fill(hex_color):
    return PatternFill(fill_type="solid", fgColor=hex_color)

def make_font(bold=False, color="000000", size=11, italic=False):
    return Font(bold=bold, color=color, size=size, italic=italic)

def make_border(style="thin"):
    s = Side(style=style)
    return Border(left=s, right=s, top=s, bottom=s)

def make_alignment(h="left", v="center", wrap=False):
    return Alignment(horizontal=h, vertical=v, wrap_text=wrap)

BORDER = make_border("thin")
BORDER_MEDIUM = Border(
    left=Side(style="medium"), right=Side(style="medium"),
    top=Side(style="medium"),  bottom=Side(style="medium")
)

def apply_header(cell, text, bg_hex, font_size=11):
    cell.value = text
    cell.fill = make_fill(bg_hex)
    cell.font = make_font(bold=True, color=C_WHITE, size=font_size)
    cell.alignment = make_alignment(h="center", v="center")
    cell.border = BORDER

def apply_data(cell, text, bg_hex=C_WHITE, bold=False, italic=False, h="left"):
    cell.value = text
    cell.fill = make_fill(bg_hex)
    cell.font = make_font(bold=bold, color="000000", size=10, italic=italic)
    cell.alignment = make_alignment(h=h, v="center", wrap=True)
    cell.border = BORDER

def set_col_widths(ws, widths):
    for col_letter, width in widths.items():
        ws.column_dimensions[col_letter].width = width

def freeze(ws, cell):
    ws.freeze_panes = cell

# ---------------------------------------------------------------------------
# 3. HOJA 1 — ÍNDICE DE TABLAS
# ---------------------------------------------------------------------------

def build_indice(wb):
    ws = wb.create_sheet("Índice de tablas")
    ws.sheet_view.showGridLines = False

    # Título
    ws.merge_cells("A1:I1")
    t = ws["A1"]
    t.value = "RetailIQ360 — Diccionario de Datos"
    t.fill = make_fill(C_HEADER_DARK)
    t.font = make_font(bold=True, color=C_WHITE, size=14)
    t.alignment = make_alignment(h="center", v="center")
    ws.row_dimensions[1].height = 30

    ws.merge_cells("A2:I2")
    s = ws["A2"]
    s.value = "Inventario de las 19 tablas del modelo: 5 dimensiones · 3 tablas de hechos · 11 benchmarks CACE"
    s.fill = make_fill("2C3E50")
    s.font = make_font(color=C_WHITE, size=10, italic=True)
    s.alignment = make_alignment(h="center", v="center")
    ws.row_dimensions[2].height = 20

    # Encabezados
    headers = ["#", "Nombre tabla", "Categoría", "Subcategoría", "Archivo", "Carpeta", "Filas aprox.", "Columnas", "Descripción"]
    color_map = {"Dimensión": C_HEADER_DIM, "Tabla de hechos": C_HEADER_FACT, "Benchmark CACE": C_HEADER_CACE}
    fill_map  = {"Dimensión": C_LIGHT_DIM,  "Tabla de hechos": C_LIGHT_FACT,  "Benchmark CACE": C_LIGHT_CACE}

    row = 4
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.fill = make_fill(C_SUBHEADER)
        c.font = make_font(bold=True, color=C_WHITE, size=10)
        c.alignment = make_alignment(h="center", v="center")
        c.border = BORDER
    ws.row_dimensions[row].height = 20

    # Datos
    for idx, tabla in enumerate(TABLAS, 1):
        row += 1
        bg = fill_map.get(tabla["categoria"], C_WHITE)
        alt = idx % 2 == 0
        row_bg = bg if not alt else bg  # mismo color por categoría (o alternar levemente)
        vals = [
            idx,
            tabla["nombre"],
            tabla["categoria"],
            tabla["subcategoria"],
            tabla["archivo"],
            tabla["carpeta"],
            tabla["filas"],
            len(tabla["columnas"]),
            tabla["descripcion"],
        ]
        for col_i, val in enumerate(vals, 1):
            c = ws.cell(row=row, column=col_i, value=val)
            c.fill = make_fill(row_bg)
            c.font = make_font(size=10, bold=(col_i == 2))
            h_align = "center" if col_i in (1, 3, 4, 7, 8) else "left"
            c.alignment = make_alignment(h=h_align, v="center", wrap=(col_i == 9))
            c.border = BORDER
        ws.row_dimensions[row].height = 35

    set_col_widths(ws, {
        "A": 5, "B": 28, "C": 18, "D": 18, "E": 38,
        "F": 28, "G": 14, "H": 10, "I": 60,
    })
    freeze(ws, "A5")
    return ws

# ---------------------------------------------------------------------------
# 4. HOJA 2 — DICCIONARIO COMPLETO
# ---------------------------------------------------------------------------

def build_diccionario(wb):
    ws = wb.create_sheet("Diccionario completo")
    ws.sheet_view.showGridLines = False

    cat_bg = {"DIM": C_HEADER_DIM, "FACT": C_HEADER_FACT, "CACE": C_HEADER_CACE}
    cat_row_bg = {"DIM": C_LIGHT_DIM, "FACT": C_LIGHT_FACT, "CACE": C_LIGHT_CACE}
    key_bg = {"PK": C_PK, "FK": C_FK, "CALC": C_CALC}

    # Título
    ws.merge_cells("A1:J1")
    t = ws["A1"]
    t.value = "RetailIQ360 — Diccionario de Datos Completo"
    t.fill = make_fill(C_HEADER_DARK)
    t.font = make_font(bold=True, color=C_WHITE, size=14)
    t.alignment = make_alignment(h="center", v="center")
    ws.row_dimensions[1].height = 30

    # Leyenda
    ws.merge_cells("A2:J2")
    leyenda = ws["A2"]
    leyenda.value = "Leyenda clave:  ◆ PK = clave primaria  |  ◇ FK = clave foránea  |  ⟳ CALC = columna calculada en Power BI"
    leyenda.fill = make_fill("2C3E50")
    leyenda.font = make_font(color=C_WHITE, size=10, italic=True)
    leyenda.alignment = make_alignment(h="center", v="center")
    ws.row_dimensions[2].height = 18

    # Encabezados columnas
    headers = [
        "Tabla", "Categoría", "N°", "Nombre columna",
        "Tipo de dato", "Clave", "Tabla relacionada", "Col. relacionada",
        "Descripción", "Notas"
    ]
    row = 4
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.fill = make_fill(C_SUBHEADER)
        c.font = make_font(bold=True, color=C_WHITE, size=10)
        c.alignment = make_alignment(h="center", v="center")
        c.border = BORDER
    ws.row_dimensions[row].height = 20

    # Filas de datos
    for tabla in TABLAS:
        cc = tabla["color_cat"]
        for col_num, (col_name, tipo, clave, rel_tabla, rel_col, desc) in enumerate(tabla["columnas"], 1):
            row += 1
            row_bg = cat_row_bg.get(cc, C_WHITE)

            # Tabla
            apply_data(ws.cell(row=row, column=1), tabla["nombre"],   row_bg, bold=True)
            # Categoría
            apply_data(ws.cell(row=row, column=2), tabla["categoria"], row_bg)
            # N°
            c_num = ws.cell(row=row, column=3, value=col_num)
            c_num.fill = make_fill(row_bg)
            c_num.font = make_font(size=10)
            c_num.alignment = make_alignment(h="center", v="center")
            c_num.border = BORDER
            # Nombre columna
            apply_data(ws.cell(row=row, column=4), col_name, row_bg, bold=(clave in ("PK",)))
            # Tipo
            apply_data(ws.cell(row=row, column=5), tipo, row_bg, h="center")
            # Clave
            k_bg = key_bg.get(clave, row_bg)
            c_k = ws.cell(row=row, column=6)
            c_k.value = clave if clave else "—"
            c_k.fill = make_fill(k_bg)
            c_k.font = make_font(size=10, bold=bool(clave))
            c_k.alignment = make_alignment(h="center", v="center")
            c_k.border = BORDER
            # Tabla relacionada
            apply_data(ws.cell(row=row, column=7), rel_tabla or "—", row_bg, italic=bool(rel_tabla))
            # Col. relacionada
            apply_data(ws.cell(row=row, column=8), rel_col or "—", row_bg, italic=bool(rel_col))
            # Descripción
            apply_data(ws.cell(row=row, column=9), desc, row_bg)
            # Notas
            nota = ""
            if clave == "CALC":
                nota = "Crear en Power BI con DAX: FORMAT([anio],\"0000\") & \"-\" & FORMAT([mes],\"00\")"
            apply_data(ws.cell(row=row, column=10), nota, row_bg, italic=True)
            ws.row_dimensions[row].height = 30

        # Separador visual entre tablas
        row += 1
        for col_i in range(1, 11):
            c = ws.cell(row=row, column=col_i)
            c.fill = make_fill(cat_bg.get(cc, C_SUBHEADER))
            c.border = BORDER
        ws.row_dimensions[row].height = 6

    set_col_widths(ws, {
        "A": 28, "B": 18, "C": 5, "D": 30,
        "E": 13, "F": 8, "G": 28, "H": 20,
        "I": 65, "J": 52,
    })
    freeze(ws, "A5")
    return ws

# ---------------------------------------------------------------------------
# 5. HOJA 3 — RELACIONES
# ---------------------------------------------------------------------------

def build_relaciones(wb):
    ws = wb.create_sheet("Relaciones del modelo")
    ws.sheet_view.showGridLines = False

    ws.merge_cells("A1:G1")
    t = ws["A1"]
    t.value = "RetailIQ360 — Relaciones del Modelo (Galaxy Schema)"
    t.fill = make_fill(C_HEADER_REL)
    t.font = make_font(bold=True, color=C_WHITE, size=13)
    t.alignment = make_alignment(h="center", v="center")
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:G2")
    s = ws["A2"]
    s.value = "Constelación AR Sintético (izq.) + Constelación Olist (der.) comparten dim_canal_ar como dimensión conformada."
    s.fill = make_fill("145A32")
    s.font = make_font(color=C_WHITE, size=10, italic=True)
    s.alignment = make_alignment(h="center", v="center")
    ws.row_dimensions[2].height = 18

    headers = ["#", "Tabla origen", "Columna origen", "Tabla destino", "Columna destino", "Cardinalidad", "Tipo", "Notas"]
    row = 4
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.fill = make_fill(C_SUBHEADER)
        c.font = make_font(bold=True, color=C_WHITE, size=10)
        c.alignment = make_alignment(h="center", v="center")
        c.border = BORDER
    ws.row_dimensions[row].height = 20

    # Agrupación por constelación
    grupos = {
        "Constelación 1 — AR Sintético": [0, 1, 2, 3, 4],
        "Constelación 2 — Olist Procesado": [5],
    }
    rel_list = RELACIONES

    # Subencabezado constelación 1
    row += 1
    ws.merge_cells(f"A{row}:H{row}")
    c = ws[f"A{row}"]
    c.value = "Constelación 1 — AR Sintético"
    c.fill = make_fill("1A5276")
    c.font = make_font(bold=True, color=C_WHITE, size=10, italic=True)
    c.alignment = make_alignment(h="left", v="center")
    ws.row_dimensions[row].height = 18

    for idx in [0, 1, 2, 3, 4]:
        row += 1
        r = rel_list[idx]
        vals = [idx + 1, r[0], r[1], r[2], r[3], r[4], r[5], r[6]]
        row_bg = C_LIGHT_DIM if idx % 2 == 0 else C_WHITE
        for col_i, val in enumerate(vals, 1):
            c = ws.cell(row=row, column=col_i, value=val)
            c.fill = make_fill(row_bg)
            c.font = make_font(size=10, bold=(col_i in (2, 3)))
            c.alignment = make_alignment(h="center" if col_i in (1, 6, 7) else "left", v="center", wrap=(col_i == 8))
            c.border = BORDER
        ws.row_dimensions[row].height = 28

    # Subencabezado constelación 2
    row += 1
    ws.merge_cells(f"A{row}:H{row}")
    c2 = ws[f"A{row}"]
    c2.value = "Constelación 2 — Olist Procesado"
    c2.fill = make_fill("145A32")
    c2.font = make_font(bold=True, color=C_WHITE, size=10, italic=True)
    c2.alignment = make_alignment(h="left", v="center")
    ws.row_dimensions[row].height = 18

    row += 1
    r = rel_list[5]
    vals = [6, r[0], r[1], r[2], r[3], r[4], r[5], r[6]]
    for col_i, val in enumerate(vals, 1):
        c = ws.cell(row=row, column=col_i, value=val)
        c.fill = make_fill(C_CALC)
        c.font = make_font(size=10, bold=(col_i in (2, 3)))
        c.alignment = make_alignment(h="center" if col_i in (1, 6, 7) else "left", v="center", wrap=(col_i == 8))
        c.border = BORDER
    ws.row_dimensions[row].height = 30

    # Nota al pie
    row += 2
    ws.merge_cells(f"A{row}:H{row}")
    nota = ws[f"A{row}"]
    nota.value = ("⚠  IMPORTANTE: dim_clientes_ar NO tiene relación formal con dim_geografia_ar. "
                  "Sus campos geográficos (provincia, ciudad, region, zona) son texto autocontenido sin FK. "
                  "Las tablas CACE tampoco tienen relaciones formales en el modelo.")
    nota.fill = make_fill("FDEBD0")
    nota.font = make_font(size=10, italic=True)
    nota.alignment = make_alignment(h="left", v="center", wrap=True)
    nota.border = BORDER
    ws.row_dimensions[row].height = 40

    set_col_widths(ws, {"A": 5, "B": 28, "C": 20, "D": 28, "E": 20, "F": 14, "G": 12, "H": 60})
    freeze(ws, "A5")
    return ws

# ---------------------------------------------------------------------------
# 6. HOJA 4 — VERIFICACIONES
# ---------------------------------------------------------------------------

def build_verificaciones(wb):
    ws = wb.create_sheet("Verificaciones")
    ws.sheet_view.showGridLines = False

    ws.merge_cells("A1:F1")
    t = ws["A1"]
    t.value = "RetailIQ360 — Checklist de Verificaciones antes de publicar en Power BI"
    t.fill = make_fill(C_HEADER_VER)
    t.font = make_font(bold=True, color=C_WHITE, size=13)
    t.alignment = make_alignment(h="center", v="center")
    ws.row_dimensions[1].height = 28

    headers = ["Estado", "Tabla", "N°", "Tipo", "Verificación", "Observaciones"]
    row = 3
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.fill = make_fill(C_SUBHEADER)
        c.font = make_font(bold=True, color=C_WHITE, size=10)
        c.alignment = make_alignment(h="center", v="center")
        c.border = BORDER
    ws.row_dimensions[row].height = 20

    tipo_bg = {"Integridad": "D5E8D4", "Negocio": "DAE8FC", "Formato": "FFF2CC"}
    cat_order = {}
    cur_cat = None

    for tabla_nombre, nro, texto, tipo in VERIFICACIONES:
        # Subencabezado por tabla
        t_info = next((t for t in TABLAS if t["nombre"] == tabla_nombre), None)
        if t_info and t_info["nombre"] != cur_cat:
            cur_cat = t_info["nombre"]
            row += 1
            ws.merge_cells(f"A{row}:F{row}")
            sub = ws[f"A{row}"]
            sub.value = f"  {t_info['nombre']}  —  {t_info['categoria']}"
            sub_bg = {"DIM": C_HEADER_DIM, "FACT": C_HEADER_FACT, "CACE": C_HEADER_CACE}.get(t_info["color_cat"], C_SUBHEADER)
            sub.fill = make_fill(sub_bg)
            sub.font = make_font(bold=True, color=C_WHITE, size=10)
            sub.alignment = make_alignment(h="left", v="center")
            ws.row_dimensions[row].height = 16

        row += 1
        row_bg = tipo_bg.get(tipo, C_WHITE)
        # Estado (checkbox vacío)
        c_st = ws.cell(row=row, column=1, value="☐")
        c_st.fill = make_fill(row_bg)
        c_st.font = Font(size=12)
        c_st.alignment = make_alignment(h="center", v="center")
        c_st.border = BORDER
        # Tabla
        apply_data(ws.cell(row=row, column=2), tabla_nombre, row_bg)
        # N°
        c_n = ws.cell(row=row, column=3, value=nro)
        c_n.fill = make_fill(row_bg)
        c_n.font = make_font(size=10)
        c_n.alignment = make_alignment(h="center", v="center")
        c_n.border = BORDER
        # Tipo
        apply_data(ws.cell(row=row, column=4), tipo, row_bg, h="center")
        # Verificación
        apply_data(ws.cell(row=row, column=5), texto, row_bg)
        # Observaciones (vacío)
        c_obs = ws.cell(row=row, column=6, value="")
        c_obs.fill = make_fill(C_WHITE)
        c_obs.border = BORDER
        ws.row_dimensions[row].height = 22

    set_col_widths(ws, {"A": 8, "B": 28, "C": 5, "D": 14, "E": 70, "F": 40})
    freeze(ws, "A4")

    # Leyenda de colores
    row += 2
    ws.merge_cells(f"A{row}:F{row}")
    leg = ws[f"A{row}"]
    leg.value = "Leyenda tipos:  🟢 Verde = Integridad referencial  |  🔵 Azul = Regla de negocio  |  🟡 Amarillo = Formato de datos"
    leg.fill = make_fill("F2F3F4")
    leg.font = make_font(size=9, italic=True)
    leg.alignment = make_alignment(h="left", v="center")
    return ws

# ---------------------------------------------------------------------------
# 7. HOJA 5 — ORDEN DE CARGA
# ---------------------------------------------------------------------------

def build_orden_carga(wb):
    ws = wb.create_sheet("Orden de carga Power BI")
    ws.sheet_view.showGridLines = False

    ws.merge_cells("A1:F1")
    t = ws["A1"]
    t.value = "RetailIQ360 — Orden recomendado de carga en Power BI"
    t.fill = make_fill(C_HEADER_DARK)
    t.font = make_font(bold=True, color=C_WHITE, size=13)
    t.alignment = make_alignment(h="center", v="center")
    ws.row_dimensions[1].height = 28

    ws.merge_cells("A2:F2")
    s = ws["A2"]
    s.value = "Cargar primero las dimensiones, luego las tablas de hechos, y por último los benchmarks CACE (sin relaciones formales)."
    s.fill = make_fill("2C3E50")
    s.font = make_font(color=C_WHITE, size=10, italic=True)
    s.alignment = make_alignment(h="center", v="center")
    ws.row_dimensions[2].height = 18

    headers = ["Paso", "Nombre tabla", "Archivo", "Carpeta", "Tipo", "Notas de carga"]
    row = 4
    for i, h in enumerate(headers, 1):
        c = ws.cell(row=row, column=i, value=h)
        c.fill = make_fill(C_SUBHEADER)
        c.font = make_font(bold=True, color=C_WHITE, size=10)
        c.alignment = make_alignment(h="center", v="center")
        c.border = BORDER
    ws.row_dimensions[row].height = 20

    notas = {
        "dim_geografia_ar":     "Cargar primero — es referenciada por dim_sucursales_ar",
        "dim_canal_ar":         "Cargar temprano — es compartida entre las dos constelaciones",
        "dim_inflacion_ipc":    "Crear columna calculada anio_mes luego de la carga",
        "dim_sucursales_ar":    "Requiere que dim_geografia_ar ya esté cargada",
        "dim_clientes_ar":      "Sin dependencias de dimensiones previas",
        "fact_ventas":          "Crear columna calculada anio_mes; NO cargar los 9 archivos raw de Olist",
        "fact_ventas_base_ar":  "Dimensiones AR deben estar cargadas antes",
        "fact_precios_comp":    "Requiere que dim_canal_ar ya esté cargada",
    }
    cace_nota = "Referencia sin relaciones formales — no conectar en Model View"

    fill_map = {"Dimensión": C_LIGHT_DIM, "Tabla de hechos": C_LIGHT_FACT, "Benchmark CACE": C_LIGHT_CACE}

    for step, tabla in enumerate(TABLAS, 1):
        row += 1
        bg = fill_map.get(tabla["categoria"], C_WHITE)
        nota = notas.get(tabla["nombre"], cace_nota if tabla["categoria"] == "Benchmark CACE" else "")
        vals = [step, tabla["nombre"], tabla["archivo"], tabla["carpeta"], tabla["categoria"], nota]
        for col_i, val in enumerate(vals, 1):
            c = ws.cell(row=row, column=col_i, value=val)
            c.fill = make_fill(bg)
            c.font = make_font(size=10, bold=(col_i in (1, 2)))
            c.alignment = make_alignment(h="center" if col_i in (1, 5) else "left", v="center", wrap=(col_i == 6))
            c.border = BORDER
        ws.row_dimensions[row].height = 28

    set_col_widths(ws, {"A": 7, "B": 30, "C": 40, "D": 28, "E": 20, "F": 60})
    freeze(ws, "A5")
    return ws

# ---------------------------------------------------------------------------
# 8. MAIN
# ---------------------------------------------------------------------------

def main():
    wb = openpyxl.Workbook()
    # Eliminar hoja por defecto
    if "Sheet" in wb.sheetnames:
        del wb["Sheet"]

    build_indice(wb)
    build_diccionario(wb)
    build_relaciones(wb)
    build_verificaciones(wb)
    build_orden_carga(wb)

    out_path = os.path.join(os.path.dirname(__file__), "diccionario_datos_RetailIQ360.xlsx")
    wb.save(out_path)
    print(f"Archivo generado: {out_path}")

if __name__ == "__main__":
    main()

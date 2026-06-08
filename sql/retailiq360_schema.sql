-- ============================================================
-- RetailIQ 360° — Script de esquema SQL completo v2
-- Base de datos: RetailIQ360
-- Generado desde diccionario_datos_RetailIQ360.xlsx
-- Tipos de dato unificados y verificados en todas las tablas
-- ============================================================
-- INSTRUCCIONES DE USO:
-- 1. Abrir SSMS y conectarse al servidor local (.)
-- 2. Ejecutar el bloque CREATE DATABASE primero
-- 3. Ejecutar el resto del script completo de una sola vez
-- 4. Importar los CSVs con el asistente (Tareas > Importar datos planos)
--    Las tablas ya existen — el asistente solo inserta los datos
-- 5. Ejecutar la query de verificacion al final para confirmar FK
-- ============================================================

-- ------------------------------------------------------------
-- CREAR BASE DE DATOS
-- ------------------------------------------------------------
CREATE DATABASE RetailIQ360
    COLLATE Latin1_General_CI_AS;  -- soporta acentos del español
GO

USE RetailIQ360;
GO


-- ============================================================
-- DIMENSIONES — orden de creacion respeta dependencias FK
-- ============================================================

-- ------------------------------------------------------------
-- DimGeografia (sin dependencias externas — va primero)
-- ------------------------------------------------------------
CREATE TABLE DimGeografia (
    GeografiaID      INT            NOT NULL,
    region           NVARCHAR(50)   NOT NULL,
    provincia        NVARCHAR(100)  NOT NULL,
    ciudad           NVARCHAR(100)  NOT NULL,
    zona             NVARCHAR(20)   NOT NULL,  -- AMBA o Interior
    peso_facturacion DECIMAL(8,4)   NOT NULL   -- suma 1.0, calibrado CACE
    CONSTRAINT PK_DimGeografia PRIMARY KEY (GeografiaID)
);
GO

-- ------------------------------------------------------------
-- DimCanal (sin dependencias externas)
-- CanalID definido como INT en todas las tablas para evitar
-- conflictos de tipo con FactVentas y FactPreciosComp
-- ------------------------------------------------------------
CREATE TABLE DimCanal (
    CanalID          INT            NOT NULL,
    nombre           NVARCHAR(100)  NOT NULL,
    tipo             NVARCHAR(50)   NOT NULL,
    plataforma       NVARCHAR(100)  NULL,      -- POS fisico | Sitio web | App | MercadoLibre
    flag_online      TINYINT        NOT NULL,  -- 0=presencial, 1=online
    peso_facturacion DECIMAL(8,4)   NOT NULL   -- suma 1.0, calibrado CACE
    CONSTRAINT PK_DimCanal PRIMARY KEY (CanalID)
);
GO

-- ------------------------------------------------------------
-- DimTiempo (sin dependencias externas)
-- PK sobre fecha (DATE). Es la Date Table del modelo.
-- es_fin_semana almacenado como TINYINT (0/1) — BIT no es
-- compatible con el asistente de importacion de CSV
-- ------------------------------------------------------------
CREATE TABLE DimTiempo (
    fecha         DATE           NOT NULL,
    TiempoID      INT            NOT NULL,  -- YYYYMMDD ej: 20171015
    anio          INT            NOT NULL,
    semestre      INT            NOT NULL,
    trimestre     INT            NOT NULL,
    mes           INT            NOT NULL,
    nombre_mes    NVARCHAR(20)   NOT NULL,
    dia           INT            NOT NULL,
    dia_semana    INT            NOT NULL,  -- 0=lunes, 6=domingo
    nombre_dia    NVARCHAR(20)   NOT NULL,
    semana_anio   INT            NOT NULL,
    es_fin_semana TINYINT        NOT NULL,  -- 0=False, 1=True
    anio_mes      NVARCHAR(10)   NOT NULL,  -- 'YYYY-MM' para ejes
    PeriodoID     INT            NOT NULL   -- YYYYMM ej: 201710
    CONSTRAINT PK_DimTiempo PRIMARY KEY (fecha)
);
GO

-- ------------------------------------------------------------
-- DimInflacion (sin dependencias externas)
-- PeriodoID = anio*100+mes. Base dic-2016 = 1.0
-- ------------------------------------------------------------
CREATE TABLE DimInflacion (
    PeriodoID                INT            NOT NULL,
    fecha                    DATE           NOT NULL,
    ipc_nivel_general        DECIMAL(10,4)  NULL,
    ipc_alimentos_bebidas    DECIMAL(10,4)  NULL,
    ipc_indumentaria_calzado DECIMAL(10,4)  NULL,
    ipc_equipamiento_hogar   DECIMAL(10,4)  NULL,
    ipc_transporte           DECIMAL(10,4)  NULL,
    ipc_comunicacion         DECIMAL(10,4)  NULL,
    anio                     INT            NULL,
    mes                      INT            NULL,
    indice_ipc_acum          DECIMAL(12,6)  NULL   -- deflactor acumulado base dic-2016
    CONSTRAINT PK_DimInflacion PRIMARY KEY (PeriodoID)
);
GO

-- ------------------------------------------------------------
-- DimCategorias (sin dependencias externas)
-- Tabla puente de 10 categorias CACE.
-- PK compuesta: CategoriaID (entero) + categoria_es (texto)
-- Las FK de otras tablas referencian categoria_es como NVARCHAR(100)
-- ------------------------------------------------------------
CREATE TABLE DimCategorias (
    CategoriaID  INT            NOT NULL,
    categoria_es NVARCHAR(100)  NOT NULL
    CONSTRAINT PK_DimCategorias PRIMARY KEY (CategoriaID),
    CONSTRAINT UQ_DimCategorias_categoria_es UNIQUE (categoria_es)
);
GO

-- ------------------------------------------------------------
-- DimSucursal (depende de DimGeografia)
-- SucursalID queda NULL en FactVentas para canales digitales.
-- Eso es correcto por diseno, no es un error.
-- ------------------------------------------------------------
CREATE TABLE DimSucursal (
    SucursalID     INT            NOT NULL,
    nombre         NVARCHAR(150)  NOT NULL,
    tipo           NVARCHAR(50)   NOT NULL,   -- Tienda grande | Tienda chica | Dark store
    GeografiaID    INT            NOT NULL,
    provincia      NVARCHAR(100)  NULL,
    ciudad         NVARCHAR(100)  NULL,
    region         NVARCHAR(50)   NULL,
    m2_ventas      INT            NULL,
    empleados      INT            NULL,
    fecha_apertura DATE           NULL,
    flag_activa    TINYINT        NOT NULL DEFAULT 1  -- 1=activa, 0=cerrada
    CONSTRAINT PK_DimSucursal PRIMARY KEY (SucursalID),
    CONSTRAINT FK_DimSucursal_DimGeografia
        FOREIGN KEY (GeografiaID) REFERENCES DimGeografia(GeografiaID)
);
GO

-- ------------------------------------------------------------
-- DimProducto (depende de DimCategorias)
-- product_id es texto Olist (hash UUID-like). NVARCHAR(50).
-- categoria_es referencia DimCategorias por UNIQUE constraint.
-- ------------------------------------------------------------
CREATE TABLE DimProducto (
    product_id            NVARCHAR(50)   NOT NULL,
    product_category_name NVARCHAR(100)  NULL,   -- categoria original en portugues
    category_en           NVARCHAR(100)  NULL,   -- 72 categorias Olist en ingles
    categoria_es          NVARCHAR(100)  NULL,   -- 10 categorias CACE en espanol
    product_weight_g      DECIMAL(10,2)  NULL,
    product_length_cm     DECIMAL(10,2)  NULL,
    product_height_cm     DECIMAL(10,2)  NULL,
    product_width_cm      DECIMAL(10,2)  NULL,
    volumen_cm3           DECIMAL(14,2)  NULL    -- CALC: largo*alto*ancho
    CONSTRAINT PK_DimProducto PRIMARY KEY (product_id),
    CONSTRAINT FK_DimProducto_DimCategorias
        FOREIGN KEY (categoria_es) REFERENCES DimCategorias(categoria_es)
);
GO

-- ------------------------------------------------------------
-- DimCliente (depende de DimGeografia)
-- segmento_rfm es 100% nulo en el modelo actual.
-- Reservada para la etapa de segmentacion RFM (etapa 2.6).
-- ------------------------------------------------------------
CREATE TABLE DimCliente (
    ClienteID       INT            NOT NULL,
    nombre          NVARCHAR(150)  NULL,
    email           NVARCHAR(200)  NULL,
    telefono        NVARCHAR(30)   NULL,
    provincia       NVARCHAR(100)  NULL,
    ciudad          NVARCHAR(100)  NULL,
    region          NVARCHAR(50)   NULL,
    zona            NVARCHAR(20)   NULL,
    nse             NVARCHAR(10)   NULL,   -- ABC1 | C2 | C3 | D
    rango_edad      NVARCHAR(20)   NULL,   -- 18-20 | 21-29 | 30-34 | 35-44 | 45-59 | 60+
    genero          CHAR(1)        NULL,   -- M | F
    canal_preferido NVARCHAR(50)   NULL,
    segmento_rfm    DECIMAL(10,4)  NULL,   -- 100% nulo, reservado para etapa RFM
    fecha_alta      DATE           NULL,
    GeografiaID     INT            NULL
    CONSTRAINT PK_DimCliente PRIMARY KEY (ClienteID),
    CONSTRAINT FK_DimCliente_DimGeografia
        FOREIGN KEY (GeografiaID) REFERENCES DimGeografia(GeografiaID)
);
GO


-- ============================================================
-- TABLAS DE HECHOS
-- Se crean despues de todas las dimensiones
-- ============================================================

-- ------------------------------------------------------------
-- FactVentas — tabla de hechos principal
-- 110.197 filas. Granularidad: 1 item vendido por fila.
-- SucursalID NULL para CanalID 2,3,4 (~92% de filas). OK por diseno.
-- PeriodoID NULL para sep-dic 2016 (~317 filas sin cobertura IPC).
-- ------------------------------------------------------------
CREATE TABLE FactVentas (
    VentaID              INT            NOT NULL,
    ClienteID            INT            NULL,
    CanalID              INT            NULL,
    SucursalID           INT            NULL,   -- NULL para canales digitales
    PeriodoID            INT            NULL,   -- NULL para sep-dic 2016 sin IPC
    fecha                DATE           NULL,
    anio                 INT            NULL,
    mes                  INT            NULL,
    trimestre            INT            NULL,
    category_en          NVARCHAR(100)  NULL,
    medio_pago           NVARCHAR(50)   NULL,
    nro_cuotas           INT            NULL,   -- 1 | 3 | 6 | 10 | 15
    tipo_entrega         NVARCHAR(50)   NULL,
    plazo_entrega        NVARCHAR(50)   NULL,
    cantidad             INT            NULL,
    precio_venta_brl     DECIMAL(14,4)  NULL,
    flete_brl            DECIMAL(14,4)  NULL,
    ars_por_usd          DECIMAL(14,4)  NULL,
    tipo_cambio          DECIMAL(14,6)  NULL,   -- CALC: ars_por_usd / 3.3
    precio_venta_ars     DECIMAL(16,2)  NULL,   -- precio nominal en ARS
    flete_ars            DECIMAL(16,2)  NULL,
    ipc_nivel_general    DECIMAL(10,4)  NULL,
    indice_ipc_acum      DECIMAL(12,6)  NULL,
    precio_venta_ars_real DECIMAL(16,2) NULL,   -- CALC: precio_venta_ars / indice_ipc_acum
    tiene_ipc            TINYINT        NULL,   -- 0=False (sep-dic 2016), 1=True
    order_id             NVARCHAR(50)   NULL,   -- ID original Olist (trazabilidad)
    product_id           NVARCHAR(50)   NULL,
    seller_id            NVARCHAR(50)   NULL    -- ID vendedor Olist (trazabilidad)
    CONSTRAINT PK_FactVentas PRIMARY KEY (VentaID),
    CONSTRAINT FK_FactVentas_DimTiempo
        FOREIGN KEY (fecha) REFERENCES DimTiempo(fecha),
    CONSTRAINT FK_FactVentas_DimCanal
        FOREIGN KEY (CanalID) REFERENCES DimCanal(CanalID),
    CONSTRAINT FK_FactVentas_DimCliente
        FOREIGN KEY (ClienteID) REFERENCES DimCliente(ClienteID),
    CONSTRAINT FK_FactVentas_DimSucursal
        FOREIGN KEY (SucursalID) REFERENCES DimSucursal(SucursalID),
    CONSTRAINT FK_FactVentas_DimInflacion
        FOREIGN KEY (PeriodoID) REFERENCES DimInflacion(PeriodoID),
    CONSTRAINT FK_FactVentas_DimProducto
        FOREIGN KEY (product_id) REFERENCES DimProducto(product_id)
);
GO

-- ------------------------------------------------------------
-- FactPreciosComp — tabla de hechos secundaria
-- 360 filas: 10 categorias x 12 meses x 3 anios (2022-2024).
-- fecha_relevamiento es siempre el dia 15 del mes.
-- precio_web_ars < precio_lista_ars en la mayoria de los casos.
-- price_index < 1 significa precio propio mas barato que competencia.
-- ------------------------------------------------------------
CREATE TABLE FactPreciosComp (
    PrecioID           INT            NOT NULL,
    categoria          NVARCHAR(100)  NOT NULL,  -- FK a DimCategorias.categoria_es
    anio               INT            NULL,
    mes                INT            NULL,
    fecha_relevamiento DATE           NULL,       -- siempre dia 15 del mes
    precio_lista_ars   DECIMAL(16,2)  NULL,
    precio_web_ars     DECIMAL(16,2)  NULL,
    precio_competencia DECIMAL(16,2)  NULL,
    descuento_pct      DECIMAL(8,4)   NULL,       -- entre 0 y 1
    price_index        DECIMAL(10,4)  NULL,       -- CALC: precio_web / precio_competencia
    CanalID            INT            NULL,
    PeriodoID          INT            NULL
    CONSTRAINT PK_FactPreciosComp PRIMARY KEY (PrecioID),
    CONSTRAINT FK_FactPreciosComp_DimCategorias
        FOREIGN KEY (categoria) REFERENCES DimCategorias(categoria_es),
    CONSTRAINT FK_FactPreciosComp_DimTiempo
        FOREIGN KEY (fecha_relevamiento) REFERENCES DimTiempo(fecha),
    CONSTRAINT FK_FactPreciosComp_DimCanal
        FOREIGN KEY (CanalID) REFERENCES DimCanal(CanalID),
    CONSTRAINT FK_FactPreciosComp_DimInflacion
        FOREIGN KEY (PeriodoID) REFERENCES DimInflacion(PeriodoID)
);
GO


-- ============================================================
-- VERIFICACION FINAL
-- Ejecutar para confirmar que las 13 FK quedaron correctas.
-- Resultado esperado: 13 filas, una por cada relacion.
-- ============================================================
SELECT
    fk.name                 AS FK_nombre,
    tp.name                 AS Tabla_origen,
    cp.name                 AS Columna_origen,
    tr.name                 AS Tabla_destino,
    cr.name                 AS Columna_destino
FROM
    sys.foreign_keys fk
    JOIN sys.foreign_key_columns fkc ON fk.object_id = fkc.constraint_object_id
    JOIN sys.tables  tp  ON fkc.parent_object_id     = tp.object_id
    JOIN sys.columns cp  ON fkc.parent_object_id     = cp.object_id
                         AND fkc.parent_column_id    = cp.column_id
    JOIN sys.tables  tr  ON fkc.referenced_object_id = tr.object_id
    JOIN sys.columns cr  ON fkc.referenced_object_id = cr.object_id
                         AND fkc.referenced_column_id = cr.column_id
ORDER BY
    tp.name, fk.name;
GO

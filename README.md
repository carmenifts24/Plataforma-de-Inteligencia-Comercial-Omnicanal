# Plataforma de Inteligencia Comercial Omnicanal

Proyecto integrador de análisis de datos comerciales con enfoque omnicanal. Integra datasets de e-commerce, logística, medios de pago y comportamiento del comprador para generar inteligencia accionable.

## Objetivo

Construir una plataforma de análisis que permita visualizar KPIs clave, detectar patrones de compra y tomar decisiones basadas en datos a través de múltiples canales de venta.

## Datasets utilizados

| Dataset | Descripción |
|---|---|
| Olist | Transacciones de e-commerce brasileño (pedidos, clientes, vendedores, reseñas) |
| Sample Superstore | Ventas retail multicanal por región y categoría |
| CACE | Indicadores del comercio electrónico argentino (KPIs, conversión, logística) |
| RetailIQ Faker | Dataset sintético generado para simulación de escenarios |
| IPC / Tipos de cambio | Contexto macroeconómico para análisis ajustado por inflación |

## Estructura del proyecto

```
integrador_carrera/
├── notebooks/          # Análisis exploratorio y modelado
├── src/                # Módulos Python reutilizables
├── datos/
│   ├── raw/            # Datos originales sin modificar
│   ├── procesados/     # Datos limpios y transformados
│   └── exportados/     # Outputs para reportes y dashboards
├── diseño/             # Diagramas del modelo de datos
├── informacion_teorica/# Bibliografía y guías de referencia
├── docs/               # Documentación del proyecto
├── requirements.txt    # Dependencias Python
└── .gitignore
```

## Tecnologías

- **Python 3.14** — lenguaje principal
- **Pandas / NumPy** — manipulación y análisis de datos
- **Matplotlib / Seaborn / Plotly** — visualización
- **Scikit-learn** — machine learning
- **JupyterLab** — entorno de desarrollo interactivo
- **Git / GitHub** — control de versiones

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/carmenifts24/Plataforma-de-Inteligencia-Comercial-Omnicanal.git
cd Plataforma-de-Inteligencia-Comercial-Omnicanal

# Instalar dependencias
pip install -r requirements.txt

# Iniciar JupyterLab
jupyter lab
```

## Modelo de datos

El proyecto utiliza un **esquema galaxia** con dos tablas de hechos:
- `fact_ventas` — transacciones y revenue
- `fact_logistica` — tiempos y tipos de entrega

Conectadas a dimensiones compartidas: tiempo, cliente, producto, región, canal y vendedor.

## Fases del proyecto

- [x] Fase 1 — Exploración y generación de datos sintéticos
- [ ] Fase 2 — Limpieza e integración de datasets
- [ ] Fase 3 — Análisis exploratorio (EDA)
- [ ] Fase 4 — Modelado y KPIs
- [ ] Fase 5 — Dashboard y presentación final

## Autora

Carmen — IFTS N° 24 | Tecnicatura en Ciencia de Datos

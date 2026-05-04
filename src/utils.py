"""Utilidades comunes para el proyecto RetailIQ 360°."""

from pathlib import Path
import pandas as pd

ROOT             = Path(__file__).parent.parent
DATOS_RAW        = ROOT / "datos" / "01_raw"
DATOS_PROCESADOS = ROOT / "datos" / "04_procesados"
DATOS_SINTETICOS = ROOT / "datos" / "03_sinteticos"
CACE_BENCHMARKS  = ROOT / "datos" / "02_cace_benchmarks"


def cargar_csv(nombre_archivo: str, carpeta: Path = DATOS_RAW, **kwargs) -> pd.DataFrame:
    """Carga un CSV desde la carpeta indicada con encoding automático."""
    ruta = carpeta / nombre_archivo
    try:
        return pd.read_csv(ruta, **kwargs)
    except UnicodeDecodeError:
        return pd.read_csv(ruta, encoding="latin-1", **kwargs)


def resumen_df(df: pd.DataFrame) -> pd.DataFrame:
    """Devuelve un resumen de columnas: tipo, nulos y % nulos."""
    resumen = pd.DataFrame({
        "tipo":      df.dtypes,
        "nulos":     df.isnull().sum(),
        "pct_nulos": (df.isnull().sum() / len(df) * 100).round(2),
        "unicos":    df.nunique(),
    })
    return resumen.sort_values("pct_nulos", ascending=False)


def guardar_procesado(df: pd.DataFrame, nombre: str) -> Path:
    """Guarda un DataFrame en datos/04_procesados."""
    DATOS_PROCESADOS.mkdir(parents=True, exist_ok=True)
    ruta = DATOS_PROCESADOS / nombre
    df.to_csv(ruta, index=False, encoding="utf-8-sig")
    print(f"Guardado en: {ruta}")
    return ruta


def guardar_sintetico(df: pd.DataFrame, nombre: str) -> Path:
    """Guarda un DataFrame en datos/03_sinteticos."""
    DATOS_SINTETICOS.mkdir(parents=True, exist_ok=True)
    ruta = DATOS_SINTETICOS / nombre
    df.to_csv(ruta, index=False, encoding="utf-8-sig")
    print(f"Guardado en: {ruta}")
    return ruta

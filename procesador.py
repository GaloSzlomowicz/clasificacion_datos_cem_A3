# -*- coding: utf-8 -*-
"""Módulo de procesamiento ETL para datos CEM A3 Mercados."""

import pandas as pd
from io import BytesIO

COLS_EXCLUIR = ["FECHA", "PRODUCTO", "TIPO CONTRATO"]


def procesar_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza un DataFrame de datos A3 Mercados al formato estándar."""
    df = df.copy()

    # FECHA: convertir a datetime y ordenar
    if "FECHA" in df.columns:
        df["FECHA"] = pd.to_datetime(df["FECHA"], format="%d-%m-%Y", errors="coerce")
        df = df.sort_values("FECHA").reset_index(drop=True)

    # Normalizar columnas numéricas (formato argentino)
    for col in df.columns:
        if col not in COLS_EXCLUIR:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("%", "", regex=False)
                .str.replace(".", "", regex=False)
                .str.replace(",", ".", regex=False)
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def cargar_archivo(file) -> pd.DataFrame:
    """Carga CSV o Excel según extensión del archivo."""
    filename = getattr(file, "filename", str(file)).lower()

    if filename.endswith(".csv"):
        return pd.read_csv(file, sep=";", encoding="utf-8", encoding_errors="ignore")
    if filename.endswith((".xlsx", ".xls")):
        return pd.read_excel(file)
    raise ValueError("Formato no soportado. Use CSV (;) o Excel (.xlsx).")


def guardar_excel(df: pd.DataFrame) -> BytesIO:
    """Guarda el DataFrame a Excel en memoria."""
    buffer = BytesIO()
    df.to_excel(buffer, index=False, engine="openpyxl")
    buffer.seek(0)
    return buffer

# -*- coding: utf-8 -*-
"""Sistema de clasificación de datos - CEM A3 Mercados.

ETL pipeline para datos de mercado argentinos (ROFEX/BYMA).
Input: CSV/Excel con formato argentino (coma decimal, punto miles).
Output: Excel limpio, ordenado y tipado correctamente.
"""

import pandas as pd
from pathlib import Path

input_path = Path("GAL.csv")
output_path = Path("GAL.xlsx")

# Cargar CSV
df = pd.read_csv(input_path, sep=";")

# Convertir FECHA a datetime y ordenar
df["FECHA"] = pd.to_datetime(df["FECHA"], format="%d-%m-%Y", errors="coerce")
df = df.sort_values("FECHA").reset_index(drop=True)

# Columnas que NO son numéricas
cols_excluir = ["FECHA", "PRODUCTO", "TIPO CONTRATO"]

# Normalizar todas las demás columnas a float con separador decimal "."
for col in df.columns:
    if col not in cols_excluir:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace("%", "", regex=False)
            .str.replace(".", "", regex=False)   # quita separadores de miles
            .str.replace(",", ".", regex=False)  # coma -> punto decimal
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

# Ensure the output directory exists
output_path.parent.mkdir(parents=True, exist_ok=True)

# Guardar a Excel con floats correctos
df.to_excel(output_path, index=False)

output_path.as_posix(), df.dtypes.to_dict(), df.head()

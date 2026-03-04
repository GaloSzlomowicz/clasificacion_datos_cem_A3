# 🗂️ Market Data ETL — Argentine Format CSV to Excel Normalizer

> Lightweight ETL pipeline that ingests raw Argentine market data (ROFEX/BYMA CSV exports) and outputs a clean, type-correct Excel file. Handles Argentine numeric conventions: comma as decimal separator, dot as thousands separator, percentage symbols.

---

## 🇬🇧 English

### Problem it solves

Argentine market data exports (ROFEX, BYMA, brokers) use locale-specific formatting that breaks standard pandas parsing:

| Raw format | Standard pandas reads it as |
|---|---|
| `1.234,56` | string |
| `15,30%` | string |
| `01-03-2025` | string (wrong format) |

This script normalizes all of it automatically.

### What it does

```
GAL.csv (raw, Argentine format)
        │
        ▼
1. Parse dates → datetime (%d-%m-%Y)
2. Sort chronologically
3. Strip % symbols
4. Convert . (thousands) → remove
5. Convert , (decimal) → .
6. Cast to float (errors → NaN)
        │
        ▼
GAL.xlsx (clean, typed, sorted)
```

### Column handling

- `FECHA` → `datetime64` (sorted ascending)
- `PRODUCTO`, `TIPO CONTRATO` → preserved as strings
- All other columns → `float64` (with Argentine format normalization)

### Requirements

```bash
pip install pandas openpyxl
```

### Usage

```bash
python sistema_de_clasificacion_de_datos.py
```

Input: `GAL.csv` (semicolon-separated, Argentine locale)
Output: `GAL.xlsx` (clean floats, sorted by date)

### Adaptable to any instrument

Change the input/output paths to process any BYMA/ROFEX export:

```python
input_path  = Path("GGAL.csv")
output_path = Path("GGAL.xlsx")
```

### Skills demonstrated

- ETL pipeline for Argentine financial data (BYMA/ROFEX format)
- Locale-aware numeric normalization (comma decimal, dot thousands)
- Robust datetime parsing with error handling
- Selective column typing (categorical vs numeric)
- pandas + openpyxl pipeline

---

## 🇦🇷 Español

### Problema que resuelve

Las exportaciones de datos de mercado argentinos (ROFEX, BYMA, brokers) usan formato de locale que rompe el parsing estándar de pandas:

| Formato crudo | pandas lo lee como |
|---|---|
| `1.234,56` | string |
| `15,30%` | string |
| `01-03-2025` | string (formato incorrecto) |

Este script normaliza todo automáticamente.

### Qué hace

```
GAL.csv (crudo, formato argentino)
        │
        ▼
1. Parsea fechas → datetime (%d-%m-%Y)
2. Ordena cronológicamente
3. Elimina símbolos %
4. Convierte . (miles) → elimina
5. Convierte , (decimal) → .
6. Castea a float (errores → NaN)
        │
        ▼
GAL.xlsx (limpio, tipado, ordenado)
```

### Skills que demuestra

- Pipeline ETL para datos financieros argentinos (formato BYMA/ROFEX)
- Normalización numérica con locale argentino (coma decimal, punto miles)
- Parsing de fechas robusto con manejo de errores
- Tipado selectivo de columnas (categóricas vs numéricas)
- Pipeline pandas + openpyxl

---

## Author

**unabomber1618** · [github.com/unabomber1618](https://github.com/unabomber1618)

> *ETL utility for Argentine market data — BYMA/ROFEX CSV exports normalized to clean Excel.*

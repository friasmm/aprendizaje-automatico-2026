"""Convierte el Cuadro 2 del IPI manufacturero (INDEC) en una tabla larga:
una fila por división y mes, lista para el análisis."""
from pathlib import Path
import pandas as pd

ENTRADA = Path("Parcial/data/raw/sh_ipi_manufacturero_2026.xls")
SALIDA = Path("Parcial/data/processed/ipi_divisiones_mensual.csv")

# Códigos de las 16 divisiones (el resto de las columnas son subclases)
DIVISIONES = ["15", "16", "17", "18-19", "20-22", "23", "24", "25",
              "26", "27", "28", "29", "30-33", "34", "35", "36-38"]

MESES = {"Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5,
         "Junio": 6, "Julio": 7, "Agosto": 8, "Septiembre": 9,
         "Octubre": 10, "Noviembre": 11, "Diciembre": 12}

crudo = pd.read_excel(ENTRADA, sheet_name="Cuadro 2", header=None)

# Fila 2 = códigos, fila 3 = nombres; las columnas 1 y 2 son año y mes
codigos = crudo.iloc[2].astype(str).str.strip()
nombres = crudo.iloc[3].astype(str).str.strip()
columnas = [i for i, c in enumerate(codigos) if c in DIVISIONES]

datos = crudo.iloc[6:].copy()
datos = datos[datos[2].isin(MESES.keys())]          # solo filas con un mes válido
datos[1] = pd.to_numeric(datos[1].astype(str).str.replace("*", "", regex=False),
                         errors="coerce").ffill()   # el año aparece solo en enero
fechas = pd.to_datetime(dict(year=datos[1].astype(int),
                             month=datos[2].map(MESES), day=1))

tabla = []
for i in columnas:
    tabla.append(pd.DataFrame({
        "fecha": fechas.values,
        "codigo_division": codigos[i],
        "division": nombres[i],
        "ipi": pd.to_numeric(datos[i], errors="coerce").values,
    }))
largo = pd.concat(tabla, ignore_index=True).sort_values(["codigo_division", "fecha"])

SALIDA.parent.mkdir(parents=True, exist_ok=True)
largo.to_csv(SALIDA, index=False)

print("Filas:", len(largo))
print("Divisiones:", largo["codigo_division"].nunique())
print("Período:", largo["fecha"].min().date(), "a", largo["fecha"].max().date())
print("Valores faltantes:", largo["ipi"].isna().sum())
print("Guardado en:", SALIDA)

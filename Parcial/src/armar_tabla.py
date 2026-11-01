"""Une el IPI por división con las variables externas en una tabla
división x mes, lista para analizar y modelar.

Regla para no usar información futura: cada fila representa el momento en
que el INDEC publica el IPI del mes t (unas 5-6 semanas después de terminado
el mes). En ese momento ya están publicados el tipo de cambio, las tasas y la
balanza comercial del mes t. La capacidad instalada se toma con un mes de
rezago (t-1), porque el archivo descargado llega a julio cuando el IPI llega
a agosto: es la opción conservadora.

Variable objetivo: 1 si el IPI de la división en t+3 es menor que en t-9
(es decir, contracción interanual dentro de 3 meses).

Se corre con:  python Parcial/src/armar_tabla.py  (desde cualquier carpeta)
"""
from pathlib import Path
import re
import numpy as np
import pandas as pd

BASE = Path(__file__).resolve().parents[1]   # carpeta Parcial/
RAW = BASE / "data/raw"
IPI = BASE / "data/processed/ipi_divisiones_mensual.csv"
CORRESP = BASE / "data/external/correspondencia_division_bloque.csv"
SALIDA = BASE / "data/processed/tabla_modelo.csv"

MESES = {"Enero": 1, "Febrero": 2, "Marzo": 3, "Abril": 4, "Mayo": 5,
         "Junio": 6, "Julio": 7, "Agosto": 8, "Septiembre": 9,
         "Octubre": 10, "Noviembre": 11, "Diciembre": 12}
HORIZONTE = 3
REZAGO_PUBLICACION_IPI = 2   # el IPI del mes t se publica en el mes t+2


def limpiar_mes(texto):
    """'Enero*' -> 1 ; 'Septiembree' -> 9 ; otra cosa -> NaN"""
    t = re.sub(r"[^A-Za-z]", "", str(texto)).capitalize()
    for nombre, n in MESES.items():
        if t.startswith(nombre[:5]):
            return n
    return np.nan


# ---------- 1. Capacidad instalada (nivel general y bloques) ----------
def leer_capacidad():
    c = pd.read_excel(RAW / "sh_capacidad_09_26.xls",
                      sheet_name="UCI - NG y bloques", header=None)
    nombres = c.iloc[2].tolist()
    anio = c[0].astype(str).str.extract(r"Año (\d{4})")[0].astype(float).ffill()
    mes = c[0].map(limpiar_mes)
    ok = mes.notna() & anio.notna() & pd.to_numeric(c[1], errors="coerce").notna()
    datos = c[ok].copy()
    datos.columns = nombres
    datos["fecha"] = pd.to_datetime(dict(year=anio[ok].astype(int),
                                         month=mes[ok].astype(int), day=1))
    datos = datos.drop(columns=["Período"]).set_index("fecha").apply(pd.to_numeric)
    datos["Papel y cartón + Edición e impresión"] = (
        datos[["Papel y cartón", "Edición e impresión"]].mean(axis=1))
    return datos  # columnas = bloques, índice = mes


# ---------- 2. Tipo de cambio mayorista (promedio mensual) ----------
def promedio_mensual(fechas, valores):
    """Promedia una serie diaria por mes y descarta el último mes si está incompleto."""
    d = pd.DataFrame({"fecha": pd.to_datetime(fechas, errors="coerce"),
                      "valor": pd.to_numeric(valores, errors="coerce")}).dropna()
    mensual = d.groupby(d["fecha"].dt.to_period("M"))["valor"].mean()
    mensual.index = mensual.index.to_timestamp()
    ultimo = d["fecha"].max()
    if (ultimo + pd.Timedelta(days=7)).month == ultimo.month:
        mensual = mensual.iloc[:-1]
    return mensual


def leer_tipo_cambio():
    # La hoja mensual tiene fechas escritas como texto ("Enero-09"); se usa la diaria.
    t = pd.read_excel(RAW / "com3500.xls", sheet_name="TCR diario y TCNPM", header=None)
    return promedio_mensual(t.iloc[4:, 2], t.iloc[4:, 3])


# ---------- 3. Tasa BADLAR bancos privados (promedio mensual) ----------
def leer_tasa():
    t = pd.read_excel(RAW / "series.xlsm", sheet_name="TASAS DE MERCADO", header=None)
    encabezado = t.iloc[8].astype(str)
    col = encabezado[encabezado.str.contains("BADLAR") &
                     encabezado.str.contains("Privados") &
                     encabezado.str.endswith("TNA")].index[0]
    return promedio_mensual(t.iloc[9:, 0], t.iloc[9:, col])


# ---------- 4. Balanza comercial (exportaciones e importaciones) ----------
def leer_balanza():
    b = pd.read_excel(RAW / "balanmensual.xls", sheet_name="FOB-CIF", header=None)
    b = b.iloc[6:].copy()
    anio = pd.to_numeric(b[0].astype(str).str.extract(r"(\d{4})")[0],
                         errors="coerce").ffill()
    mes = b[1].map(limpiar_mes)
    ok = mes.notna() & pd.to_numeric(b[2], errors="coerce").notna()
    d = pd.DataFrame({
        "fecha": pd.to_datetime(dict(year=anio[ok].astype(int),
                                     month=mes[ok].astype(int), day=1)),
        "expo": pd.to_numeric(b.loc[ok, 2]),
        "impo": pd.to_numeric(b.loc[ok, 7]),
    })
    return d.set_index("fecha")


def var_ia(serie):
    """Variación interanual en proporción (0.05 = +5%)."""
    return serie / serie.shift(12) - 1


# ---------- Armado ----------
ipi = pd.read_csv(IPI, parse_dates=["fecha"], dtype={"codigo_division": str})
corresp = pd.read_csv(CORRESP, dtype={"codigo_division": str})

# Variables propias del IPI (por división)
ipi = ipi.sort_values(["codigo_division", "fecha"])
g = ipi.groupby("codigo_division")["ipi"]
ipi["ipi_var_ia"] = g.transform(var_ia)
ipi["ipi_var_ia_lag1"] = ipi.groupby("codigo_division")["ipi_var_ia"].shift(1)
ipi["ipi_var_ia_lag2"] = ipi.groupby("codigo_division")["ipi_var_ia"].shift(2)
ipi["ipi_var_ia_cambio3m"] = ipi["ipi_var_ia"] - ipi.groupby("codigo_division")["ipi_var_ia"].shift(3)
ipi["contraccion_hoy"] = (ipi["ipi"] < g.shift(12)).astype(float)
ipi.loc[g.shift(12).isna(), "contraccion_hoy"] = np.nan

# Objetivo: IPI en t+3 vs. t+3-12
futuro = g.shift(-HORIZONTE)
base = g.shift(12 - HORIZONTE)
ipi["objetivo"] = (futuro < base).astype(float)
ipi.loc[futuro.isna() | base.isna(), "objetivo"] = np.nan

# Disponibilidad temporal (devolución Entrega 1):
# - mes_decision: mes en que se publica el IPI de t y se hace la predicción.
# - mes_etiqueta_conocida: mes en que se publica el IPI de t+3, es decir,
#   cuando el resultado de esa predicción ya se puede verificar.
ipi["mes_decision"] = ipi["fecha"] + pd.DateOffset(months=REZAGO_PUBLICACION_IPI)
ipi["mes_etiqueta_conocida"] = ipi["fecha"] + pd.DateOffset(
    months=HORIZONTE + REZAGO_PUBLICACION_IPI)
ipi["estado_etiqueta"] = np.where(ipi["objetivo"].notna(), "observada",
                                  np.where(futuro.isna(), "pendiente", "sin_base"))

# Capacidad instalada del bloque y nivel general, con rezago de 1 mes
uci = leer_capacidad()
uci_rez = uci.shift(1, freq="MS")
uci_dif = (uci - uci.shift(12)).shift(1, freq="MS")
ipi = ipi.merge(corresp[["codigo_division", "bloque_capacidad"]], on="codigo_division")
ipi["uci_bloque"] = [uci_rez.at[f, b] if f in uci_rez.index else np.nan
                     for f, b in zip(ipi["fecha"], ipi["bloque_capacidad"])]
ipi["uci_bloque_dif_ia"] = [uci_dif.at[f, b] if f in uci_dif.index else np.nan
                            for f, b in zip(ipi["fecha"], ipi["bloque_capacidad"])]
generales = pd.DataFrame({"uci_general": uci_rez["Nivel general"],
                          "uci_general_dif_ia": uci_dif["Nivel general"]})

# Variables macro (iguales para todas las divisiones)
tc = leer_tipo_cambio()
tasa = leer_tasa()
bal = leer_balanza()
macro = pd.DataFrame({
    "tc_var_ia": var_ia(tc),
    "tc_var_3m": tc / tc.shift(3) - 1,
    "badlar": tasa,
    "badlar_dif_ia": tasa - tasa.shift(12),
    "expo_var_ia": var_ia(bal["expo"]),
    "impo_var_ia": var_ia(bal["impo"]),
}).join(generales, how="outer")

tabla = ipi.merge(macro, left_on="fecha", right_index=True, how="left")
tabla = tabla.sort_values(["codigo_division", "fecha"]).reset_index(drop=True)

SALIDA.parent.mkdir(parents=True, exist_ok=True)
tabla.to_csv(SALIDA, index=False)

# ---------- Resumen ----------
util = tabla.dropna(subset=["objetivo", "ipi_var_ia"])
print("Filas totales:", len(tabla))
print("Filas con objetivo y variación interanual:", len(util))
print("Período utilizable:", util["fecha"].min().date(), "a", util["fecha"].max().date())
print("Proporción de contracción (objetivo=1): %.1f%%" % (100 * util["objetivo"].mean()))
print("\nDatos faltantes en las filas utilizables:")
print(util.isna().sum()[lambda s: s > 0].to_string())
print("\nEtiquetas:", tabla["estado_etiqueta"].value_counts().to_dict())
print("\nGuardado en:", SALIDA.relative_to(BASE.parent))

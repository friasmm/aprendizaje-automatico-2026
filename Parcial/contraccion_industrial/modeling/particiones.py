"""Separación temporal de la tabla división x mes, respetando:
1. Que en entrenamiento solo entren filas cuyo resultado (IPI de t+5) ya
   estaba publicado en el momento del corte.
2. Que todas las divisiones de un mismo mes queden del mismo lado
   (los filtros son siempre por fecha, nunca por posición de fila).
3. Que en evaluación solo entren predicciones con resultado observado;
   las demás quedan pendientes.
"""
import pandas as pd

from contraccion_industrial.config import PREDICTORAS


def excluir_sin_historia(tabla, predictoras=PREDICTORAS):
    """Tratamiento de faltantes (devolución Entrega 2): se excluyen los
    primeros meses de la serie, que no tienen historia suficiente para
    calcular rezagos y diferencias interanuales. No se imputa nada.

    Se excluye el mes completo (las 16 divisiones) desde el inicio de la
    serie hasta el último mes con alguna predictora faltante, y se verifica
    que después de ese mes no quede ningún faltante. Así la regla depende
    solo del pasado de cada fila y no de información futura.
    """
    incompletas = tabla[predictoras].isna().any(axis=1)
    ultimo_mes_incompleto = tabla.loc[incompletas, "fecha"].max()
    resto = tabla[tabla["fecha"] > ultimo_mes_incompleto]
    assert not resto[predictoras].isna().any().any(), "Quedan faltantes después del período excluido"
    return resto, tabla[tabla["fecha"] <= ultimo_mes_incompleto]


def separar_por_corte(tabla, corte, fin_evaluacion=None):
    """Simula estar parado al comienzo del mes `corte`.

    entrenamiento: filas cuya etiqueta se conocía antes del corte
                   (mes_etiqueta_conocida < corte).
    evaluacion:    predicciones hechas desde el corte en adelante
                   (mes_decision >= corte), con etiqueta observada y,
                   si se indica, hechas antes de `fin_evaluacion`.
    pendientes:    predicciones desde el corte cuya etiqueta aún no existe.
    """
    corte = pd.Timestamp(corte)
    observada = tabla["objetivo"].notna()
    entrenamiento = tabla[observada & (tabla["mes_etiqueta_conocida"] < corte)]
    desde_corte = tabla["mes_decision"] >= corte
    if fin_evaluacion is not None:
        desde_corte &= tabla["mes_decision"] < pd.Timestamp(fin_evaluacion)
    evaluacion = tabla[desde_corte & observada]
    pendientes = tabla[desde_corte & tabla["estado_etiqueta"].eq("pendiente")]
    return entrenamiento, evaluacion, pendientes


def cortes_validacion(tabla, cortes, duracion_meses=12):
    """Validación temporal dentro del período de entrenamiento: para cada
    corte, entrena con lo conocido antes y valida las predicciones de los
    `duracion_meses` siguientes."""
    for corte in cortes:
        fin = pd.Timestamp(corte) + pd.DateOffset(months=duracion_meses)
        ent, val, _ = separar_por_corte(tabla, corte, fin_evaluacion=fin)
        yield pd.Timestamp(corte), ent, val


def comprobar_meses_enteros(*conjuntos):
    """Verifica que ningún mes quede repartido entre dos conjuntos."""
    meses = [set(c["fecha"]) for c in conjuntos]
    for i in range(len(meses)):
        for j in range(i + 1, len(meses)):
            comunes = meses[i] & meses[j]
            assert not comunes, f"Meses repartidos entre conjuntos: {sorted(comunes)[:3]}"
    return True

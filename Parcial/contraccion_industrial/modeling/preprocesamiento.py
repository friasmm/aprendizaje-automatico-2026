"""Preparación de las entradas para los modelos (devolución Entrega 2).

Las predictoras combinan proporciones (variaciones interanuales), puntos
porcentuales (capacidad instalada, BADLAR), un nivel en % y una variable
binaria. Para la regresión logística y, sobre todo, para KNN (que mide
distancias) hay que llevarlas a una escala comparable.

El escalado se arma dentro de un Pipeline de scikit-learn: cuando se llama a
fit() con el entrenamiento de un corte, la media y el desvío (o la mediana y
el rango intercuartílico) se calculan SOLO con esas filas, y después se
aplican sin cambios a la validación o evaluación de ese corte.

Valores extremos: no se recortan. Los de la pandemia (abr-may 2020, abr 2021)
son datos reales y pueden contener información. Como opción se ofrece el
escalado robusto (mediana e IQR), que no deja que esos pocos extremos
definan la escala del resto; cuál conviene se decide con la validación
temporal, dentro del entrenamiento.
"""
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import RobustScaler, StandardScaler

ESCALADORES = {"estandar": StandardScaler, "robusto": RobustScaler}

# Modelos que necesitan escalado (los árboles no dependen de la escala)
NECESITAN_ESCALADO = {"logistica", "knn"}


def armar_pipeline(modelo, nombre_modelo, escalado="estandar"):
    """Devuelve escalado + modelo si el modelo lo necesita; si no, solo el modelo."""
    pasos = []
    if nombre_modelo in NECESITAN_ESCALADO:
        pasos.append(("escalado", ESCALADORES[escalado]()))
    pasos.append(("modelo", modelo))
    return Pipeline(pasos)

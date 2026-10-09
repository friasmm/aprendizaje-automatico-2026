# Semana 6

## Clase 6: Aprendizaje Supervisado (III) – SVM y SGD

Actividad obligatoria: comparación de dos modelos de clasificación sobre un dataset propio.

**Problema:** predecir si una persona asalariada es informal (no tiene descuento jubilatorio).

**Modelos:** Regresión Logística y Support Vector Machine (SVM).

**Datos:** microdatos de la Encuesta Permanente de Hogares (EPH), primer trimestre de 2026. Fuente: Instituto Nacional de Estadística y Censos (INDEC).

## Contenido

- `Datos/`: base individual y de hogares de la EPH y diseño de registro.
- `Notebooks/informalidad_eph_lr_vs_svm.ipynb`: análisis exploratorio, entrenamiento y comparación de los modelos.

## Resultados principales

| Modelo | Exactitud | Recall (informal) | F1 (informal) | AUC-ROC |
|---|---|---|---|---|
| Regresión Logística | 0,819 | 0,797 | 0,776 | 0,895 |
| SVM (kernel RBF) | 0,822 | 0,805 | 0,781 | 0,903 |

Los dos modelos superan claramente al modelo de referencia (que predice siempre "formal" y acierta el 60,6%). El SVM es apenas mejor, pero se elige la Regresión Logística por ser más rápida y mucho más fácil de interpretar.

## Video

[Ver el video de la actividad](video_semana6.mp4)

# Proyecto parcial — Anticipar la contracción de la industria manufacturera

**Alumna:** Mónica Frías — Aprendizaje Automático, Tecnicatura Superior en Ciencia de Datos e IA (2026)

**Objetivo:** anticipar qué divisiones de la industria manufacturera argentina van a estar en **contracción interanual 3 meses después del momento de la predicción**, usando solo información publicada en ese momento. Es un problema de **clasificación binaria**: la variable objetivo vale 1 si el índice de producción (IPI) de la división en *t+5* es menor que el del mismo mes del año anterior (*t-7*). Como el IPI de *t* se publica en *t+2*, que es cuando se toma la decisión, el mes predicho (*t+5*) queda 3 meses después, y su resultado se conoce en *t+7*.

---

## Entregas

| Entrega | Documento | Material |
|---|---|---|
| 1. Descripción y formulación del objetivo | [`docs/01_descripcion_objetivo.md`](docs/01_descripcion_objetivo.md) | — |
| 2. Descripción del dataset y origen | [`docs/02_descripcion_dataset_y_origen.md`](docs/02_descripcion_dataset_y_origen.md) | [notebook](notebooks/1.0-mf-carga-exploracion-dataset.ipynb), [tabla de modelado](data/processed/tabla_modelo.csv), [gráficos](reports/figures) |

La Entrega 2 fue corregida según la devolución del profesor; el detalle de los cambios está al comienzo del notebook.

## Fuentes de datos

Datos públicos del **INDEC** (índice de producción industrial manufacturero, capacidad instalada, balanza comercial) y del **BCRA** (tipo de cambio mayorista y tasa BADLAR). Enlaces, fechas de descarga y calendario de publicación en [`docs/02_descripcion_dataset_y_origen.md`](docs/02_descripcion_dataset_y_origen.md).

## Modelos

Regresión logística, árbol de decisión, random forest, gradient boosting y KNN, comparados con un modelo de referencia (la división sigue igual que en el último dato publicado), con validación temporal. Se desarrollan en la próxima etapa.

---

## Estructura del proyecto

Organizado según la plantilla [Cookiecutter Data Science](https://github.com/drivendataorg/cookiecutter-data-science):

```
Parcial/
├── README.md                   → este archivo
├── requirements.txt            → dependencias y versiones
├── data/
│   ├── raw/                    → datos originales, sin modificar
│   ├── interim/                → (sin uso por ahora)
│   ├── processed/              → ipi_divisiones_mensual.csv, tabla_modelo.csv
│   └── external/               → correspondencia divisiones ↔ bloques; datos de establecimientos (contexto)
├── docs/                       → documentos de cada entrega
├── models/                     → modelos entrenados (próxima etapa)
├── notebooks/
│   └── 1.0-mf-carga-exploracion-dataset.ipynb
├── references/                 → metodologías del INDEC
├── reports/
│   └── figures/                → gráficos generados por el notebook
└── contraccion_industrial/     → código del proyecto
    ├── config.py               → rutas, horizonte de predicción y lista de predictoras
    ├── dataset.py              → IPI del INDEC a formato largo
    ├── features.py             → variables, objetivo y tabla de modelado
    └── modeling/
        ├── particiones.py      → faltantes y separación temporal
        └── preprocesamiento.py → escalado para regresión logística y KNN
```

## Reproducción

Dependencias en [`requirements.txt`](requirements.txt), con las versiones usadas para ejecutar el notebook (Python 3.10). Desde la carpeta `Parcial/`:

```bash
pip install -r requirements.txt
python -m contraccion_industrial.dataset
python -m contraccion_industrial.features
jupyter notebook notebooks/1.0-mf-carga-exploracion-dataset.ipynb
```

`xlrd` es necesario para leer los `.xls` del INDEC y del BCRA, y `openpyxl` para `series.xlsm`. El notebook vuelve a correr los dos scripts, así que alcanza con abrirlo y ejecutarlo completo.

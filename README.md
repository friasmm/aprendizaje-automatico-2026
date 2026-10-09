# Aprendizaje Automático — 2026

Repositorio con los trabajos prácticos y el proyecto parcial de la materia **Aprendizaje Automático**, de la Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial (cursada 2026).

**Alumna:** Mónica Frías

## Contenido

| Carpeta | Clase | Tema | Datos |
|---|---|---|---|
| [Semana_2](Semana_2) | Clase 2 | Adquisición, inspección y visualización de datos | Automóviles, ventas, clientes e inventario |
| [Semana_4](Semana_4) | Clase 4 | Aprendizaje supervisado: regresión lineal y regresión logística | Capacidad instalada industrial (INDEC) y usuarios de un sitio web |
| [Semana_6](Semana_6) | Clase 6 | Clasificación: Regresión Logística vs. SVM | Encuesta Permanente de Hogares (INDEC), 1er trimestre 2026 |
| [Parcial](Parcial) | — | Proyecto parcial: anticipar la contracción de la actividad industrial | Índice de producción industrial manufacturero (INDEC) |

## Estructura del repositorio

Cada semana tiene su propia carpeta con los datos, las notebooks y un README con el detalle de la actividad. El proyecto parcial sigue la plantilla *Cookiecutter Data Science*.

```
aprendizaje-automatico-2026/
├── Semana_2/
│   ├── Datos/
│   ├── Notebooks/
│   └── README.md
├── Semana_4/
│   ├── Datos/
│   ├── Notebooks/
│   └── README.md
├── Semana_6/
│   ├── Datos/
│   ├── Notebooks/
│   ├── README.md
│   └── video_semana6.mp4
├── Parcial/
│   ├── data/
│   │   ├── raw/         → datos originales, sin modificar
│   │   ├── processed/   → datos preparados para el modelo
│   │   └── external/    → datos de otras fuentes, de respaldo
│   ├── references/      → metodologías de las fuentes de datos
│   └── src/             → scripts de preparación de datos
├── .gitignore           → archivos que Git no debe subir
└── README.md            → este archivo
```

Las notebooks leen los datos de la carpeta `Datos/` de su misma semana, con rutas relativas (`../Datos/...`). Para ejecutarlas hay que mantener esta estructura.

## Trabajos prácticos

### Semana 2 — Adquisición, inspección y visualización de datos

Notebook: [Clase2_Adquisicion_Visualizacion_Frias_Monica.ipynb](Semana_2/Notebooks/Clase2_Adquisicion_Visualizacion_Frias_Monica.ipynb) ([versión PDF](Semana_2/Notebooks/Clase2_Adquisicion_Visualizacion_Frias_Monica.pdf))

- **Ejercicio 1:** simulación de un análisis de mercado para un comercio electrónico. Se generan y combinan datos de ventas (CSV), clientes (JSON) e inventario (Excel). Los datos son sintéticos y se crean desde la propia notebook con una semilla fija, así que siempre resultan iguales.
- **Ejercicio 2:** exploración visual del dataset `Automobile.csv` (características de automóviles y su consumo de combustible) con gráficos de dispersión, histogramas y diagramas de caja.

### Semana 4 — Regresión lineal

Notebook: [Clase4_Regresion_Lineal_Frias_Monica.ipynb](Semana_4/Notebooks/Clase4_Regresion_Lineal_Frias_Monica.ipynb)

Pronóstico de la **utilización de la capacidad instalada de la industria** del mes siguiente a partir de los datos de los sectores industriales del mes actual.

- Preparación de los datos publicados por el INDEC y análisis exploratorio.
- Un modelo de regresión lineal simple (sector automotriz) y uno multivariado (los 4 sectores de mayor peso en la industria).
- División en entrenamiento y prueba; evaluación con MAE, MSE, R² y varianza explicada; cálculo de residuos; visualización 2D y 3D; regresión Ridge.

### Semana 4 — Regresión logística

Notebook: [Clase4_Regresion_Logistica_Frias_Monica.ipynb](Semana_4/Notebooks/Clase4_Regresion_Logistica_Frias_Monica.ipynb)

Clasificación del **sistema operativo** (Windows, Macintosh o Linux) de los usuarios que visitan un sitio web, a partir de datos de Google Analytics.

- Preparación de los datos y análisis exploratorio (distribución de clases, histogramas, diagramas de caja por sistema operativo y correlaciones).
- División en entrenamiento y prueba estratificada; estandarización de variables y modelo de regresión logística multiclase.
- Evaluación con accuracy, matriz de confusión, precision, recall, F1-score y validación cruzada; predicción para usuarios nuevos.

### Semana 6 — Regresión Logística vs. SVM

Notebook: [informalidad_eph_lr_vs_svm.ipynb](Semana_6/Notebooks/informalidad_eph_lr_vs_svm.ipynb) · [Video de la presentación](https://youtu.be/J5V4tQAIzK8)

Predicción de la **informalidad laboral** de las personas asalariadas en Argentina (si tienen o no descuento jubilatorio), comparando dos modelos de clasificación.

- Selección de 8 variables predictoras numéricas y categóricas, y exclusión de las variables que generan fuga de información.
- Análisis exploratorio de la tasa de informalidad por tamaño del establecimiento, sector, nivel educativo y región.
- Regresión Logística y SVM (kernel lineal y RBF), con búsqueda de hiperparámetros y validación cruzada.
- Evaluación con exactitud, precisión, recall, F1, AUC-ROC y matriz de confusión, contra un modelo de referencia.
- Resultado: los dos modelos rinden casi igual (F1 de 0,776 y 0,781); se elige la Regresión Logística por ser más rápida e interpretable.

## Proyecto parcial

**Tema:** anticipar qué ramas de la industria manufacturera argentina van a estar en contracción interanual dentro de los próximos tres meses (clasificación binaria).

**Estado:** propuesta presentada en el foro, a la espera de la devolución del profesor. Los datos ya están descargados y preparados.

- `Parcial/data/raw/sh_ipi_manufacturero_2026.xls`: serie original del IPI manufacturero (enero 2016 a agosto 2026).
- `Parcial/src/preparar_ipi.py`: convierte la planilla en una tabla con una fila por división y mes.
- `Parcial/data/processed/ipi_divisiones_mensual.csv`: tabla resultante, con 16 divisiones y 128 meses (2.048 filas).
- `Parcial/data/external/`: datos de establecimientos productivos del CEP XXI (2021-2022), de una idea anterior que se conserva como respaldo.

Para regenerar la tabla procesada, desde la raíz del repositorio:

```bash
python Parcial/src/preparar_ipi.py
```

## Fuentes de los datos

| Archivo | Fuente |
|---|---|
| `Automobile.csv` | Dataset de características y consumo de combustible de automóviles (modelos 1970-1982), con las mismas columnas que el dataset *Auto MPG* del UCI Machine Learning Repository. |
| `ventas.csv`, `clientes.json`, `inventario.xlsx` | Datos sintéticos generados por la notebook de la Clase 2. |
| `sh_capacidad_09_26.xls` | INDEC — *Utilización de la capacidad instalada en la industria, nivel general y bloques sectoriales. Años 2016-2026*. Descargado el 27/09/2026 de https://www.indec.gob.ar/Nivel4/Tema/3/6/15 |
| `usuarios_win_mac_lin.csv` | Provisto por la cátedra (Clase 4, Actividad 2): datos de ejemplo de visitas a un sitio web tomados de Google Analytics. |
| `usu_individual_T126.txt`, `usu_hogar_T126.txt` | INDEC — Encuesta Permanente de Hogares, bases de microdatos del 1er trimestre de 2026. https://www.indec.gob.ar/Institucional/Indec/BasesDeDatos |
| `sh_ipi_manufacturero_2026.xls` | INDEC — Índice de producción industrial manufacturero, series históricas 2016-2026. https://www.indec.gob.ar/ftp/cuadros/economia/sh_ipi_manufacturero_2026.xls |
| `Parcial/data/external/*.csv` | CEP XXI (Ministerio de Economía) — *Distribución geográfica de los establecimientos productivos*. Licencia Creative Commons Attribution 4.0. |

## Cómo ejecutar las notebooks

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/friasmm/aprendizaje-automatico-2026.git
   cd aprendizaje-automatico-2026
   ```
2. Tener instalado Python 3 con las librerías `pandas`, `numpy`, `matplotlib`, `seaborn`, `scikit-learn`, `openpyxl` y `xlrd` (todas vienen con Anaconda, salvo `xlrd` en algunas versiones: `pip install xlrd`).
3. Abrir Jupyter con `jupyter notebook`, entrar a la carpeta `Notebooks/` de la semana deseada y ejecutar la notebook.

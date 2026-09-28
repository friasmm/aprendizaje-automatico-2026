# Aprendizaje Automático — 2026

Repositorio con los trabajos prácticos de la materia **Aprendizaje Automático** (cursada 2026).

**Alumna:** Mónica Frías

## Estructura del repositorio

```
aprendizaje-automatico-2026/
├── datos/        → archivos de datos que usan las notebooks
├── notebooks/    → notebooks de Jupyter (.ipynb) con las actividades de cada clase
└── README.md     → este archivo
```

Las notebooks leen los datos desde la carpeta `datos/` con rutas relativas (`../datos/...`). Por eso, para ejecutarlas hay que mantener esta estructura de carpetas.

## Trabajos prácticos

| Clase | Tema | Notebook | Datos |
|---|---|---|---|
| **Clase 2** | Adquisición, inspección y visualización de datos | [Clase2_Adquisicion_Visualizacion_Frias_Monica.ipynb](notebooks/Clase2_Adquisicion_Visualizacion_Frias_Monica.ipynb) ([versión PDF](notebooks/Clase2_Adquisicion_Visualizacion_Frias_Monica.pdf)) | [Automobile.csv](datos/Automobile.csv), [ventas.csv](datos/ventas.csv), [clientes.json](datos/clientes.json), [inventario.xlsx](datos/inventario.xlsx) |
| **Clase 4** | Aprendizaje supervisado: regresión lineal | [Clase4_Regresion_Lineal_Frias_Monica.ipynb](notebooks/Clase4_Regresion_Lineal_Frias_Monica.ipynb) | [sh_capacidad_09_26.xls](datos/sh_capacidad_09_26.xls) |

### Clase 2 — Adquisición, inspección y visualización de datos

- **Ejercicio 1:** simulación de un análisis de mercado para un comercio electrónico. Se generan y combinan datos de ventas (CSV), clientes (JSON) e inventario (Excel). Los datos son sintéticos y se crean desde la propia notebook con una semilla fija, así que siempre resultan iguales.
- **Ejercicio 2:** exploración visual del dataset `Automobile.csv` (características de automóviles y su consumo de combustible) con gráficos de dispersión, histogramas y diagramas de caja.

### Clase 4 — Regresión lineal

Pronóstico de la **utilización de la capacidad instalada de la industria** del mes siguiente a partir de los datos de los sectores industriales del mes actual. Incluye:

- Preparación de los datos publicados por el INDEC y análisis exploratorio.
- Un modelo de regresión lineal simple (sector automotriz) y uno multivariado (los 4 sectores de mayor peso en la industria).
- División en entrenamiento y prueba; evaluación con MAE, MSE, R² y varianza explicada; cálculo de residuos; visualización 2D y 3D; regresión Ridge.

## Fuentes de los datos

| Archivo | Fuente |
|---|---|
| `sh_capacidad_09_26.xls` | INDEC — *Utilización de la capacidad instalada en la industria, nivel general y bloques sectoriales. Años 2016-2026*. Descargado el 27/09/2026 de https://www.indec.gob.ar/Nivel4/Tema/3/6/15 |
| `Automobile.csv` | Dataset de características y consumo de combustible de automóviles (modelos 1970-1982), con las mismas columnas que el dataset *Auto MPG* del UCI Machine Learning Repository. |
| `ventas.csv`, `clientes.json`, `inventario.xlsx` | Datos sintéticos generados por la notebook de la Clase 2. |

## Cómo ejecutar las notebooks

1. Clonar el repositorio:
   ```bash
   git clone https://github.com/friasmm/aprendizaje-automatico-2026.git
   cd aprendizaje-automatico-2026
   ```
2. Tener instalado Python 3 con las librerías `pandas`, `numpy`, `matplotlib`, `scikit-learn`, `openpyxl` y `xlrd` (todas vienen con Anaconda, salvo `xlrd` en algunas versiones: `pip install xlrd`).
3. Abrir Jupyter con `jupyter notebook`, entrar a la carpeta `notebooks/` y ejecutar la notebook deseada.

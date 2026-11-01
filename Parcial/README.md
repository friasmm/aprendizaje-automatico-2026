# Proyecto parcial — Anticipar la contracción de la industria manufacturera

**Alumna:** Mónica Frías — Aprendizaje Automático, Tecnicatura Superior en Ciencia de Datos e IA (2026)

**Objetivo:** anticipar qué divisiones de la industria manufacturera argentina van a estar en **contracción interanual dentro de 3 meses**, usando solo información publicada al momento de la predicción. Es un problema de **clasificación binaria**: la variable objetivo vale 1 si el índice de producción (IPI) de la división en *t+3* es menor que el del mismo mes del año anterior.

---

## Entrega 2 — Descripción del dataset y origen

| Qué | Dónde |
|---|---|
| Notebook de carga, exploración y transformaciones (ejecutado) | [`notebooks/01_carga_exploracion_dataset.ipynb`](notebooks/01_carga_exploracion_dataset.ipynb) |
| Dataset final para modelar | [`data/processed/tabla_modelo.csv`](data/processed/tabla_modelo.csv) |
| Datos originales, sin modificar | [`data/raw/`](data/raw) |
| Correspondencia divisiones ↔ bloques de capacidad | [`data/external/correspondencia_division_bloque.csv`](data/external/correspondencia_division_bloque.csv) |
| Scripts de preparación | [`src/`](src) |

### 1. Origen de los datos

Todos los datos son **de dominio público**, publicados por el INDEC y el Banco Central (BCRA). Se descargaron manualmente desde los sitios oficiales y se guardan sin modificar en `data/raw/`.

| Archivo | Contenido | Organismo | Enlace de descarga | Fecha de descarga | Período |
|---|---|---|---|---|---|
| `sh_ipi_manufacturero_2026.xls` | Índice de producción industrial manufacturero (IPI) por división y subclase, base 2004=100 (hoja *Cuadro 2*) | INDEC | https://www.indec.gob.ar/ftp/cuadros/economia/sh_ipi_manufacturero_2026.xls | 07/10/2026 | ene-2016 a ago-2026 |
| `sh_capacidad_09_26.xls` | Utilización de la capacidad instalada en la industria: nivel general y 12 bloques sectoriales (%) — publicación de septiembre 2026 | INDEC | https://www.indec.gob.ar/ftp/cuadros/economia/sh_capacidad_09_26.xls | 25/10/2026 | ene-2016 a jul-2026 |
| `balanmensual.xls` | Balanza comercial: exportaciones e importaciones mensuales, millones de USD | INDEC | https://www.indec.gob.ar/ftp/cuadros/economia/balanmensual.xls | 25/10/2026 | ene-1990 a sep-2026 |
| `com3500.xls` | Tipo de cambio de referencia Com. "A" 3500 (mayorista), diario, y promedio mensual | BCRA | https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/com3500.xls | 25/10/2026 | mar-2002 a oct-2026 |
| `series.xlsm` | Series monetarias y financieras; se usa la hoja *TASAS DE MERCADO* (BADLAR bancos privados) | BCRA | https://www.bcra.gob.ar/archivos/Pdfs/PublicacionesEstadisticas/series.xlsm | 25/10/2026 | ene-2003 a oct-2026 |

Páginas de referencia:
- IPI manufacturero: informes técnicos del INDEC (cada informe enlaza el cuadro `sh_ipi_manufacturero_AAAA.xls`). Metodología en [`references/metodologia_ipi_manufacturero_2019.pdf`](references/metodologia_ipi_manufacturero_2019.pdf) y [`references/nota_metodologica_ipi_manufacturero_2025.pdf`](references/nota_metodologica_ipi_manufacturero_2025.pdf).
- Tipo de cambio: https://www.bcra.gob.ar/tipo-cambio-referencia-comunicacion-a-3500-tcnpm/

**Calendario de publicación** (determina qué información está disponible al predecir):
- IPI del mes *t*: se publica en el mes *t+2* (por ejemplo, agosto 2026 en el informe de octubre 2026).
- Capacidad instalada del mes *t*: se publica en *t+2*. Por prudencia se usa con un mes de rezago adicional.
- Balanza comercial del mes *t*: se publica en *t+1*.
- Tipo de cambio y tasas: publicación diaria.

### 2. Preprocesamiento

Los archivos originales son planillas para leer, no para procesar: encabezados repartidos en varias filas, el año escrito una sola vez, asteriscos de dato provisorio, notas al pie y algunos errores (por ejemplo, el mes "Septiembree" en la balanza, o fechas escritas como texto en la hoja mensual del tipo de cambio). Todo se resuelve con dos scripts, que se pueden volver a correr cuando se actualicen los datos:

```bash
python Parcial/src/preparar_ipi.py   # IPI → data/processed/ipi_divisiones_mensual.csv
python Parcial/src/armar_tabla.py    # une todo → data/processed/tabla_modelo.csv
```

1. **IPI**: se toman las 16 divisiones de la hoja *Cuadro 2* y se pasan a formato largo (una fila por división y mes).
2. **Variables del IPI**: variación interanual de *t*, *t-1* y *t-2*; cambio de la variación interanual en 3 meses; indicador de contracción actual.
3. **Variable objetivo**: 1 si IPI(*t+3*) < IPI(*t-9*).
4. **Capacidad instalada**: cada división toma la de su bloque sectorial (ver punto 4) y la del nivel general, con rezago de un mes; nivel y diferencia interanual.
5. **Tipo de cambio**: promedio mensual calculado desde la serie diaria (coincide con el promedio oficial, p. ej. agosto 2026: 1.499,96); variación interanual y de 3 meses.
6. **Tasa BADLAR** (bancos privados, TNA): promedio mensual de la serie diaria; nivel y diferencia interanual. Se descarta el último mes si está incompleto.
7. **Balanza comercial**: variación interanual de exportaciones e importaciones.
8. **Columnas de disponibilidad temporal** (ver punto 5).

Se usan variaciones interanuales porque eliminan la estacionalidad y la tendencia inflacionaria de las series nominales.

### 3. Descripción del dataset final

`data/processed/tabla_modelo.csv`

- **Instancias:** 2.048 (16 divisiones × 128 meses, enero 2016 a agosto 2026). Cada fila es **una división en un mes**.
- **Filas modelables:** 1.808 (enero 2017 a mayo 2026), con variable objetivo observada y variación interanual calculable.
- **Columnas:** 24.
- **Clases:** 53,6% con objetivo = 1 (contracción), con fuerte variación entre años (del 15% en 2021 al 85% en 2018).

| Columna | Tipo | Descripción |
|---|---|---|
| `fecha` | fecha | Mes de referencia del dato del IPI (*t*) |
| `codigo_division` | texto | Código de la división (CLaNAE 2004) |
| `division` | texto | Nombre de la división |
| `ipi` | decimal | IPI, base 2004=100 |
| `ipi_var_ia` | decimal | Variación interanual del IPI en *t* (proporción) |
| `ipi_var_ia_lag1` | decimal | Variación interanual en *t-1* |
| `ipi_var_ia_lag2` | decimal | Variación interanual en *t-2* |
| `ipi_var_ia_cambio3m` | decimal | Cambio de la variación interanual respecto de *t-3* |
| `contraccion_hoy` | binaria | 1 si la división está en contracción interanual en *t* |
| **`objetivo`** | **binaria** | **1 si IPI(*t+3*) < IPI(*t-9*)** |
| `mes_decision` | fecha | Mes en que se publica el IPI de *t* y se predice (*t+2*) |
| `mes_etiqueta_conocida` | fecha | Mes en que se publica el IPI de *t+3* y se conoce el resultado (*t+5*) |
| `estado_etiqueta` | texto | `observada` / `pendiente` (aún no publicada) / `sin_base` (falta *t-9*) |
| `bloque_capacidad` | texto | Bloque de capacidad instalada asignado |
| `uci_bloque` | decimal | Capacidad instalada del bloque en *t-1* (%) |
| `uci_bloque_dif_ia` | decimal | Diferencia interanual de la capacidad del bloque (puntos) |
| `uci_general` | decimal | Capacidad instalada, nivel general, en *t-1* (%) |
| `uci_general_dif_ia` | decimal | Diferencia interanual del nivel general (puntos) |
| `tc_var_ia` | decimal | Variación interanual del tipo de cambio mayorista promedio |
| `tc_var_3m` | decimal | Variación del tipo de cambio en 3 meses |
| `badlar` | decimal | BADLAR bancos privados, promedio mensual (TNA %) |
| `badlar_dif_ia` | decimal | Diferencia interanual de la BADLAR (puntos) |
| `expo_var_ia` | decimal | Variación interanual de las exportaciones |
| `impo_var_ia` | decimal | Variación interanual de las importaciones |

**Faltantes:** solo al comienzo de la serie (las variaciones interanuales necesitan 12 meses previos) y al final (resultados a 3 meses todavía no publicados). **Valores extremos:** las variaciones de abril-mayo 2020 y abril 2021 (cierre por la pandemia y rebote) son reales; se conservan y se tratarán al modelar.

### 4. Correspondencia entre divisiones y bloques de capacidad instalada

El INDEC publica la capacidad instalada en 12 bloques, que no coinciden uno a uno con las 16 divisiones del IPI:

| División IPI | Bloque de capacidad | Criterio |
|---|---|---|
| 15 Alimentos y bebidas | Productos alimenticios y bebidas | directa |
| 16 Productos de tabaco | Productos del tabaco | directa |
| 17 Productos textiles | Productos textiles | directa |
| 18-19 Prendas de vestir, cuero y calzado | Productos textiles | aproximada (sin bloque propio) |
| 20-22 Madera, papel, edición e impresión | Promedio de Papel y cartón + Edición e impresión | promedio (madera sin bloque) |
| 23 Refinación del petróleo | Refinación del petróleo | directa |
| 24 Sustancias y productos químicos | Sustancias y productos químicos | directa (el bloque excluye farmacéutica) |
| 25 Caucho y plástico | Productos de caucho y plástico | directa |
| 26 Minerales no metálicos | Productos minerales no metálicos | directa |
| 27 Metálicas básicas | Industrias metálicas básicas | directa |
| 28 Productos de metal | Metalmecánica excl. automotriz | bloque agregado |
| 29 Maquinaria y equipo | Metalmecánica excl. automotriz | bloque agregado |
| 30-33 Otros equipos e instrumentos | Metalmecánica excl. automotriz | bloque agregado |
| 34 Vehículos automotores | Industria automotriz | directa |
| 35 Otro equipo de transporte | Metalmecánica excl. automotriz | bloque agregado |
| 36-38 Muebles y otras | Nivel general | sin bloque |

En la exploración (solo entrenamiento), la diferencia interanual de la capacidad del bloque muestra la relación esperada con la contracción en 15 de las 16 divisiones, incluidas las dos asignaciones aproximadas.

### 5. Disponibilidad temporal y separación de los datos

Atendiendo a la devolución de la Entrega 1 (implementado en [`src/particiones.py`](src/particiones.py)):

- **El resultado de cada fila no se conoce enseguida.** Una fila de diciembre 2024 se predice en febrero 2025 y su resultado (IPI de marzo 2025) se conoce en mayo 2025. El entrenamiento solo incluye filas con `mes_etiqueta_conocida` anterior al corte.
- **Los meses no se reparten entre conjuntos.** Todas las separaciones filtran por fecha, nunca por posición de fila; una verificación automática lo comprueba.
- **Predicciones sin resultado** (junio a agosto 2026) quedan como pendientes.

| Conjunto | Filas | Datos de |
|---|---|---|
| Entrenamiento (corte enero 2025) | 1.456 | 01/2017 a 07/2024 |
| Evaluación final (predicciones 2025-2026) | 304 | 11/2024 a 05/2026 |
| Pendientes | 48 | 06/2026 a 08/2026 |

La selección de variables y modelos se hace con **validación temporal dentro del entrenamiento** (cortes en enero 2021, 2022, 2023 y 2024), con las mismas reglas.

**Modelo de referencia:** predice que en 3 meses la división estará igual que en el último dato publicado (`contraccion_hoy`). En la validación temporal obtiene F1 promedio 0,52: muy bueno en tendencias estables y malo en los cambios de ciclo.

### 6. Limitaciones

- **Series revisadas, no versiones históricas.** Se usan los datos tal como estaban publicados en octubre 2026. Los datos provisorios (marcados con asterisco) pueden haber sido revisados después de su primera publicación, así que en el pasado la información disponible podía ser algo distinta. Respetar el retraso de publicación no elimina este efecto.
- **Sin datos de inflación:** la tasa BADLAR es nominal y el tipo de cambio no está ajustado por precios.
- **Variables macro con un valor por mes:** son iguales para las 16 divisiones y su relación con el objetivo se apoya en pocos ciclos económicos (2018-2019, 2020, 2023-2024).
- **Correspondencia aproximada** para las divisiones 18-19 y 36-38.

---

## Estructura de la carpeta

```
Parcial/
├── data/
│   ├── raw/          → datos originales, sin modificar
│   ├── processed/    → ipi_divisiones_mensual.csv, tabla_modelo.csv
│   └── external/     → correspondencia de bloques y datos de establecimientos (contexto)
├── notebooks/        → 01_carga_exploracion_dataset.ipynb
├── references/       → metodologías del INDEC
└── src/              → preparar_ipi.py, armar_tabla.py, particiones.py
```

Los archivos de `data/external/` sobre establecimientos productivos por departamento (CEP) se descargaron como contexto y no forman parte de la tabla de modelado.

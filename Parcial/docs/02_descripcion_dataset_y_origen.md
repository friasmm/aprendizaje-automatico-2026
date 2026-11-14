# Entrega 2 — Descripción del dataset y origen

**Proyecto:** anticipar la contracción interanual de las divisiones de la industria manufacturera argentina. **Alumna:** Mónica Frías.

Versión corregida según la devolución de la Entrega 2 (horizonte de predicción, faltantes, escalado, variaciones interanuales, quintiles y documentación).

| Qué | Dónde |
|---|---|
| Notebook de carga, exploración, transformaciones y preparación (ejecutado) | [`notebooks/1.0-mf-carga-exploracion-dataset.ipynb`](../notebooks/1.0-mf-carga-exploracion-dataset.ipynb) |
| Dataset final para modelar | [`data/processed/tabla_modelo.csv`](../data/processed/tabla_modelo.csv) |
| Datos originales, sin modificar | [`data/raw/`](../data/raw) |
| Correspondencia divisiones ↔ bloques de capacidad | [`data/external/correspondencia_division_bloque.csv`](../data/external/correspondencia_division_bloque.csv) |
| Código de preparación | [`contraccion_industrial/`](../contraccion_industrial) |
| Gráficos de la exploración | [`reports/figures/`](../reports/figures) |

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
- IPI manufacturero: informes técnicos del INDEC (cada informe enlaza el cuadro `sh_ipi_manufacturero_AAAA.xls`). Metodología en [`references/metodologia_ipi_manufacturero_2019.pdf`](../references/metodologia_ipi_manufacturero_2019.pdf) y [`references/nota_metodologica_ipi_manufacturero_2025.pdf`](../references/nota_metodologica_ipi_manufacturero_2025.pdf).
- Tipo de cambio: https://www.bcra.gob.ar/tipo-cambio-referencia-comunicacion-a-3500-tcnpm/

**Calendario de publicación** (determina qué información está disponible al predecir):
- IPI del mes *t*: se publica en el mes *t+2* (por ejemplo, agosto 2026 en el informe de octubre 2026).
- Capacidad instalada del mes *t*: se publica en *t+2*. Por prudencia se usa con un mes de rezago adicional.
- Balanza comercial del mes *t*: se publica en *t+1*.
- Tipo de cambio y tasas: publicación diaria.

### 2. Preprocesamiento

Los archivos originales son planillas para leer, no para procesar: encabezados repartidos en varias filas, el año escrito una sola vez, asteriscos de dato provisorio, notas al pie y algunos errores (por ejemplo, el mes "Septiembree" en la balanza, o fechas escritas como texto en la hoja mensual del tipo de cambio). Todo se resuelve con el módulo `contraccion_industrial/`, que se puede volver a correr cuando se actualicen los datos (desde la carpeta `Parcial/`):

```bash
python -m contraccion_industrial.dataset    # IPI → data/processed/ipi_divisiones_mensual.csv
python -m contraccion_industrial.features   # une todo → data/processed/tabla_modelo.csv
```

1. **IPI**: se toman las 16 divisiones de la hoja *Cuadro 2* y se pasan a formato largo (una fila por división y mes).
2. **Variables del IPI**: variación interanual de *t*, *t-1* y *t-2*; cambio de la variación interanual en 3 meses; indicador de contracción actual.
3. **Variable objetivo**: 1 si IPI(*t+5*) < IPI(*t-7*).
4. **Capacidad instalada**: cada división toma la de su bloque sectorial (ver punto 4) y la del nivel general, con rezago de un mes; nivel y diferencia interanual.
5. **Tipo de cambio**: promedio mensual calculado desde la serie diaria (coincide con el promedio oficial, p. ej. agosto 2026: 1.499,96); variación interanual y de 3 meses.
6. **Tasa BADLAR** (bancos privados, TNA): promedio mensual de la serie diaria; nivel y diferencia interanual. Se descarta el último mes si está incompleto.
7. **Balanza comercial**: variación interanual de exportaciones e importaciones.
8. **Columnas de disponibilidad temporal** (ver punto 5).

**Sobre las variaciones interanuales.** Comparar cada mes con el mismo mes del año anterior **reduce** parte del efecto estacional y pone en escala comparable series de niveles muy distintos, pero hay que distinguir:
- **Crecimiento interanual** (lo que se usa): no garantiza eliminar la estacionalidad, porque cambios en días hábiles, feriados o en el patrón estacional de un sector siguen afectando la comparación.
- **Ajuste estacional** (por ejemplo, X-13 ARIMA-SEATS): procedimiento específico que estima y quita el componente estacional. No se aplicó.
- **Ajuste por precios**: deflactar una serie nominal por un índice de precios. No se aplicó: la variación interanual del tipo de cambio (`tc_var_ia`) sigue siendo **nominal**, igual que la BADLAR. El IPI es un índice de volumen físico y no lo necesita.

9. **Faltantes**: se excluyen los primeros meses sin historia suficiente para rezagos y diferencias interanuales (enero-marzo 2017, 48 filas), sin imputar; la función `excluir_sin_historia` de `contraccion_industrial/modeling/particiones.py` verifica que después no quede ningún faltante.
10. **Escalado** (`contraccion_industrial/modeling/preprocesamiento.py`): para regresión logística y KNN, escalado dentro de un `Pipeline`, ajustado solo con el entrenamiento de cada corte temporal. Estándar por defecto y robusto (mediana e IQR) como alternativa a evaluar en la validación. Los valores extremos de la pandemia no se recortan.

### 3. Descripción del dataset final

`data/processed/tabla_modelo.csv`

- **Instancias:** 2.048 (16 divisiones × 128 meses, enero 2016 a agosto 2026). Cada fila es **una división en un mes**.
- **Filas modelables:** 1.728 (abril 2017 a marzo 2026), con variable objetivo observada y sin faltantes en las predictoras (de 1.776 filas con objetivo y variación interanual, se excluyen las 48 de enero-marzo 2017).
- **Columnas:** 24.
- **Clases:** 54,9% con objetivo = 1 (contracción), con fuerte variación entre años (del 18% en 2021 al 94% en 2018).

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
| **`objetivo`** | **binaria** | **1 si IPI(*t+5*) < IPI(*t-7*)** |
| `mes_decision` | fecha | Mes en que se publica el IPI de *t* y se predice (*t+2*) |
| `mes_etiqueta_conocida` | fecha | Mes en que se publica el IPI de *t+5* y se conoce el resultado (*t+7*) |
| `estado_etiqueta` | texto | `observada` / `pendiente` (aún no publicada) / `sin_base` (falta *t-7*) |
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

**Faltantes:** solo al comienzo de la serie (las variaciones interanuales y los rezagos necesitan meses previos) y al final (resultados de *t+5* todavía no publicados); tratamiento en el punto 2.9. **Valores extremos:** las variaciones de abril-mayo 2020 y abril 2021 (cierre por la pandemia y rebote) son reales y se conservan, sin recortar.

### 4. Correspondencia entre divisiones y bloques de capacidad instalada

El INDEC publica la capacidad instalada en 12 bloques, que no coinciden uno a uno con las 16 divisiones del IPI:

| División IPI | Bloque de capacidad | Criterio |
|---|---|---|
| 15 Alimentos y bebidas | Productos alimenticios y bebidas | directa |
| 16 Productos de tabaco | Productos del tabaco | directa |
| 17 Productos textiles | Productos textiles | directa |
| 18-19 Prendas de vestir, cuero y calzado | Productos textiles | aproximada (sin bloque propio) |
| 20-22 Madera, papel, edición e impresión | Promedio simple de Papel y cartón + Edición e impresión | aproximación propia (ver nota) |
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

**Nota sobre 20-22:** el promedio simple de los dos bloques es una **aproximación propia**, no una medición oficial del INDEC para la división: no está ponderado por el peso de cada bloque y no incluye la madera, que no tiene bloque propio.

En la exploración (solo entrenamiento), la diferencia interanual de la capacidad del bloque muestra la relación esperada con la contracción en las 16 divisiones (en tabaco, muy débil), incluidas las asignaciones aproximadas. Esa asociación predictiva favorable **no demuestra** que los sectores asignados sean equivalentes.

### 5. Disponibilidad temporal y separación de los datos

Atendiendo a las devoluciones de las Entregas 1 y 2 (implementado en [`contraccion_industrial/modeling/particiones.py`](../contraccion_industrial/modeling/particiones.py)):

- **Horizonte.** Una fila de diciembre 2024 se predice en febrero 2025 (cuando se publica su IPI), el objetivo es mayo 2025 (3 meses después de la decisión) y el resultado se conoce en julio 2025. El entrenamiento solo incluye filas con `mes_etiqueta_conocida` anterior al corte.
- **Los meses no se reparten entre conjuntos.** Todas las separaciones filtran por fecha, nunca por posición de fila; una verificación automática lo comprueba.
- **Predicciones sin resultado** (filas de abril a agosto 2026) quedan como pendientes.

| Conjunto | Filas | Datos de |
|---|---|---|
| Entrenamiento (corte enero 2025) | 1.376 | 04/2017 a 05/2024 |
| Evaluación final (predicciones 2025-2026) | 272 | 11/2024 a 03/2026 |
| Pendientes | 80 | 04/2026 a 08/2026 |

Las filas de junio a octubre 2024 no entran en ninguno de los dos: sus predicciones se hicieron en 2024, pero los resultados se conocieron en 2025.

La selección de variables y modelos se hace con **validación temporal dentro del entrenamiento** (cortes en enero 2021, 2022, 2023 y 2024), con las mismas reglas.

**Modelo de referencia:** predice que 3 meses después de la decisión la división estará igual que en el último dato publicado (`contraccion_hoy`). En la validación temporal obtiene F1 promedio 0,51 (0,24 / 0,30 / 0,61 / 0,88): muy bueno en tendencias estables y malo en los cambios de ciclo.

### 6. Limitaciones

- **Series revisadas, no versiones históricas.** Se usan los datos tal como estaban publicados en octubre 2026. Los datos provisorios (marcados con asterisco) pueden haber sido revisados después de su primera publicación, así que en el pasado la información disponible podía ser algo distinta. Respetar el retraso de publicación no elimina este efecto.
- **Sin ajuste por precios ni ajuste estacional:** la BADLAR y la variación del tipo de cambio son nominales (con inflación alta, parte de su variación refleja la suba general de precios), y las variaciones interanuales reducen pero no eliminan la estacionalidad.
- **Variables macro con un valor por mes:** son iguales para las 16 divisiones y su relación con el objetivo se apoya en pocos ciclos económicos (2018-2019, 2020, 2023-2024).
- **Correspondencia aproximada** para las divisiones 18-19, 20-22 (promedio propio) y 36-38.

Los archivos de `data/external/` sobre establecimientos productivos por departamento (CEP) se descargaron como contexto y no forman parte de la tabla de modelado.

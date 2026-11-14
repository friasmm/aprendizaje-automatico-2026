# Diccionario de datos

Proyecto: anticipar la contracción interanual de las divisiones de la industria manufacturera argentina.

Este diccionario describe los archivos de `data/processed/` y `data/external/` que usa el proyecto. Los archivos originales de `data/raw/` se describen en [`docs/02_descripcion_dataset_y_origen.md`](../docs/02_descripcion_dataset_y_origen.md): fuentes, enlaces, fechas de descarga y calendario de publicación.

**Convención de tiempo.** Cada fila corresponde a una división en un mes *t*, que es el mes del dato del IPI. Ese dato se publica en *t+2*, que es cuando se hace la predicción. El mes que se predice es *t+5*, 3 meses después de la decisión, y su resultado se conoce en *t+7*.

---

## 1. `data/processed/tabla_modelo.csv` — tabla de modelado

- **Unidad de análisis:** división industrial × mes.
- **Filas:** 2.048 (16 divisiones × 128 meses, enero 2016 a agosto 2026).
- **Columnas:** 24.
- **Generada por:** `contraccion_industrial/features.py`.

La columna **Rol** indica para qué se usa cada variable:

| Rol | Significado |
|---|---|
| ID | Identifica la fila |
| Control | Separación temporal de los datos; no se usa para predecir |
| Predictora | Entra en los modelos |
| Objetivo | Lo que se predice |
| Auxiliar | Sirve para calcular otras columnas o para describir; no entra en los modelos |

Los rangos y los faltantes están calculados sobre la tabla completa.

### Identificación

| Columna | Rol | Tipo | Unidad | Descripción | Fuente | Rango / valores | Faltantes |
|---|---|---|---|---|---|---|---|
| `fecha` | ID | fecha | mes | Mes de referencia del dato del IPI (*t*). Siempre el día 1. | — | 01/2016 a 08/2026 | 0 |
| `codigo_division` | ID | texto | — | Código de la división según la CLaNAE 2004 (ver sección 3). | INDEC | 16 valores | 0 |
| `division` | ID | texto | — | Nombre de la división. | INDEC | 16 valores | 0 |
| `bloque_capacidad` | Auxiliar | texto | — | Bloque de capacidad instalada asignado a la división (ver sección 2). | Asignación propia | 12 valores | 0 |

### Variables del IPI (por división)

Fuente: INDEC, IPI manufacturero, hoja *Cuadro 2* (`sh_ipi_manufacturero_2026.xls`). Todas se conocen en *t+2*.

| Columna | Rol | Tipo | Unidad | Descripción / cálculo | Rango observado | Faltantes |
|---|---|---|---|---|---|---|
| `ipi` | Auxiliar | decimal | índice, base 2004 = 100 | Índice de producción industrial de la división en *t*. Mide volumen físico. | 14,5 a 216,9 | 0 |
| `ipi_var_ia` | Predictora | decimal | proporción (0,05 = +5%) | Variación interanual: IPI(*t*) / IPI(*t-12*) − 1. | −0,89 a 7,55 | 192 |
| `ipi_var_ia_lag1` | Predictora | decimal | proporción | Variación interanual de *t-1*. | −0,89 a 7,55 | 208 |
| `ipi_var_ia_lag2` | Predictora | decimal | proporción | Variación interanual de *t-2*. | −0,89 a 7,55 | 224 |
| `ipi_var_ia_cambio3m` | Predictora | decimal | diferencia de proporciones | Aceleración: `ipi_var_ia`(*t*) − `ipi_var_ia`(*t-3*). | −7,09 a 7,39 | 240 |
| `contraccion_hoy` | Predictora (y modelo de referencia) | binaria | 0 / 1 | 1 si IPI(*t*) < IPI(*t-12*), es decir, si la división está en contracción interanual en el último dato publicado. | 0 / 1 | 192 |

Los valores extremos (+755%, −89%) son reales: corresponden al cierre de abril-mayo de 2020 y al rebote de abril de 2021 contra esa base casi nula. No se corrigen.

### Variable objetivo y control temporal

| Columna | Rol | Tipo | Unidad | Descripción / cálculo | Rango / valores | Faltantes |
|---|---|---|---|---|---|---|
| **`objetivo`** | **Objetivo** | binaria | 0 / 1 | **1 si IPI(*t+5*) < IPI(*t-7*)**: contracción interanual del mes *t+5*, 3 meses después de la decisión. | 0 / 1 | 192 (ver `estado_etiqueta`) |
| `mes_decision` | Control | fecha | mes | *t+2*: se publica el IPI de *t* y se hace la predicción. | 03/2016 a 10/2026 | 0 |
| `mes_etiqueta_conocida` | Control | fecha | mes | *t+7*: se publica el IPI de *t+5* y se conoce el resultado. Una fila entra en el entrenamiento solo si este mes es anterior al corte. | 08/2016 a 03/2027 | 0 |
| `estado_etiqueta` | Control | texto | — | `observada`: el objetivo ya se conoce (1.856 filas). `pendiente`: el IPI de *t+5* todavía no se publicó (80 filas, abril a agosto 2026). `sin_base`: no hay dato de *t-7* (112 filas, enero a julio 2016). | 3 valores | 0 |

### Capacidad instalada

Fuente: INDEC, utilización de la capacidad instalada en la industria (`sh_capacidad_09_26.xls`, hoja *UCI - NG y bloques*). Se usa con un mes de rezago (dato de *t-1*), por prudencia: así queda disponible con seguridad en *t+2*.

| Columna | Rol | Tipo | Unidad | Descripción / cálculo | Rango observado | Faltantes |
|---|---|---|---|---|---|---|
| `uci_bloque` | Predictora | decimal | % | Utilización de la capacidad del bloque asignado, en *t-1*. Para 20-22 es el promedio simple de dos bloques: una aproximación propia (ver sección 2). | 0,0 a 97,1 | 16 |
| `uci_bloque_dif_ia` | Predictora | decimal | puntos porcentuales | Diferencia interanual: `uci_bloque`(*t-1*) − `uci_bloque`(*t-13*). | −58,6 a 65,7 | 208 |
| `uci_general` | Predictora | decimal | % | Utilización de la capacidad, nivel general de la industria, en *t-1*. Es igual para las 16 divisiones de un mes. | 42,0 a 69,6 | 16 |
| `uci_general_dif_ia` | Predictora | decimal | puntos porcentuales | Diferencia interanual del nivel general. | −19,6 a 21,2 | 208 |

### Variables macroeconómicas

Tienen un solo valor por mes, igual para las 16 divisiones. Todas están publicadas en *t+2*.

| Columna | Rol | Tipo | Unidad | Descripción / cálculo | Fuente | Rango observado | Faltantes |
|---|---|---|---|---|---|---|---|
| `tc_var_ia` | Predictora | decimal | proporción | Variación interanual del tipo de cambio mayorista de referencia (Com. A 3500), promedio mensual calculado desde la serie diaria. Es **nominal**. | BCRA, `com3500.xls` | 0,04 a 3,49 | 0 |
| `tc_var_3m` | Predictora | decimal | proporción | Variación del tipo de cambio promedio contra 3 meses antes. Nominal. | BCRA, `com3500.xls` | −0,06 a 1,36 | 0 |
| `badlar` | Predictora | decimal | % TNA | Tasa BADLAR de bancos privados, promedio mensual de la serie diaria. Nominal. | BCRA, `series.xlsm` (hoja *TASAS DE MERCADO*) | 19,2 a 129,4 | 0 |
| `badlar_dif_ia` | Predictora | decimal | puntos porcentuales | Diferencia interanual de la BADLAR. | BCRA, `series.xlsm` | −93,2 a 60,2 | 0 |
| `expo_var_ia` | Predictora | decimal | proporción | Variación interanual de las exportaciones FOB (millones de USD). | INDEC, `balanmensual.xls` | −0,36 a 0,86 | 0 |
| `impo_var_ia` | Predictora | decimal | proporción | Variación interanual de las importaciones CIF (millones de USD). | INDEC, `balanmensual.xls` | −0,37 a 0,79 | 0 |

### Faltantes y filas modelables

- Los faltantes de las variables interanuales y de los rezagos están al **comienzo** de la serie: hacen falta 12 a 15 meses previos.
- Los faltantes del objetivo están al comienzo (`sin_base`) y al **final** (`pendiente`).
- **Filas modelables:** 1.728. Son las filas con objetivo observado y sin faltantes en las predictoras, de abril 2017 a marzo 2026. Enero a marzo de 2017 se excluyen por falta de historia, sin imputar (función `excluir_sin_historia` de `contraccion_industrial/modeling/particiones.py`).

---

## 2. `data/external/correspondencia_division_bloque.csv` — divisiones y bloques de capacidad

Asignación propia: el INDEC publica la capacidad instalada en 12 bloques, que no coinciden uno a uno con las 16 divisiones del IPI.

| Columna | Tipo | Descripción |
|---|---|---|
| `codigo_division` | texto | Código de la división del IPI |
| `division` | texto | Nombre de la división |
| `bloque_capacidad` | texto | Bloque de capacidad instalada asignado |
| `criterio` | texto | `directa`, `aproximada`, `promedio` o `bloque agregado` (ver detalle en `docs/02`, sección 4) |

**Nota sobre 20-22 (Madera, papel, edición e impresión).** Se usa el promedio simple de los bloques *Papel y cartón* y *Edición e impresión*. Es una aproximación propia, no una medición oficial: no está ponderada y no incluye la madera, que no tiene bloque propio.

---

## 3. `data/processed/ipi_divisiones_mensual.csv` — IPI en formato largo

Paso intermedio generado por `contraccion_industrial/dataset.py` a partir de la hoja *Cuadro 2* del IPI.

| Columna | Tipo | Descripción |
|---|---|---|
| `fecha` | fecha | Mes de referencia |
| `codigo_division` | texto | Código de la división |
| `division` | texto | Nombre de la división |
| `ipi` | decimal | Índice de producción industrial, base 2004 = 100 |

**Divisiones (CLaNAE 2004):**

| Código | División |
|---|---|
| 15 | Alimentos y bebidas |
| 16 | Productos de tabaco |
| 17 | Productos textiles |
| 18-19 | Prendas de vestir, cuero y calzado |
| 20-22 | Madera, papel, edición e impresión |
| 23 | Refinación del petróleo, coque y combustible nuclear |
| 24 | Sustancias y productos químicos |
| 25 | Productos de caucho y plástico |
| 26 | Productos minerales no metálicos |
| 27 | Industrias metálicas básicas |
| 28 | Productos de metal |
| 29 | Maquinaria y equipo |
| 30-33 | Otros equipos, aparatos e instrumentos |
| 34 | Vehículos automotores, carrocerías, remolques y autopartes |
| 35 | Otro equipo de transporte |
| 36-38 | Muebles y colchones, y otras industrias manufactureras |

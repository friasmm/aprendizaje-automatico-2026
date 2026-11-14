# Anticipar la contracción de la actividad industrial en Argentina por rama de actividad

**Entrega 1: Descripción y formulación del objetivo**

Aprendizaje Automático · Tecnicatura Superior en Ciencia de Datos e Inteligencia Artificial
Alumna: Mónica Frías · Docente: Nicolás Caballero · Octubre de 2026

> Versión en Markdown de la entrega del 26/10/2026. El texto es el original, salvo el objetivo específico 2, que se reformuló según la devolución. Los cambios hechos después de las devoluciones de las Entregas 1 y 2 están resumidos en la [sección 9](#9-actualizaciones-posteriores-a-la-entrega).

---

## 1. Contexto y relevancia

La industria manufacturera es uno de los sectores que más empleo formal genera en Argentina y uno de los más sensibles a los cambios en la economía. La demanda interna, el tipo de cambio, el costo del financiamiento y la competencia de los productos importados afectan de forma distinta a cada rama de actividad: un mismo contexto puede favorecer a unas y perjudicar a otras.

En los últimos meses la situación fue muy cambiante. Según el INDEC, el índice de producción industrial manufacturero cayó 5,7% en mayo de 2026 y subió 2,0% en junio. Además, las ramas no se comportan igual: en agosto de 2026, 11 de las 16 divisiones de la industria produjeron menos que en agosto de 2025. Las caídas más fuertes se dieron en Maquinaria y equipo (-24%), Otros equipos, aparatos e instrumentos (-21%) y Prendas de vestir, cuero y calzado (-15%). En cambio, Otro equipo de transporte creció 12%.

Poder anticipar qué ramas van a estar en contracción en los próximos meses es útil para empresas, cámaras sectoriales y organismos públicos que necesitan planificar con tiempo: producción, compras, empleo, financiamiento o políticas de apoyo sectorial.

## 2. Problema

Quiero construir un modelo que, para cada rama de la industria y cada mes, prediga si esa rama va a estar en contracción interanual dentro de tres meses. La predicción se hace con la información disponible en el momento: los factores económicos que influyen sobre la industria (capacidad instalada, tipo de cambio, tasa de interés e importaciones) y, como complemento, la evolución reciente de la propia rama.

## 3. Objetivo general

Desarrollar un modelo de aprendizaje automático que, a partir de factores económicos que influyen sobre la industria y de la evolución reciente de cada rama, anticipe con tres meses de horizonte si cada una de las 16 divisiones de la industria manufacturera argentina presentará una caída interanual de su producción.

## 4. Objetivos específicos

1. Integrar en una única base mensual, por división, la producción industrial y las variables explicativas, usando para cada mes solo información que ya estaba publicada en ese momento.
2. Explorar, mediante un análisis exploratorio, la relación de las variables predictoras con la variable objetivo y evaluar su aporte predictivo; la selección de variables se hace dentro del período de entrenamiento. *(Reformulado según la devolución de la Entrega 1; el original decía "verificar que las variables predictoras guardan relación con la variable objetivo, y descartar las que no aporten información".)*
3. Describir cómo evolucionó la producción de cada división desde 2016 e identificar períodos de expansión y contracción.
4. Entrenar y comparar distintos modelos de clasificación, ajustando sus hiperparámetros, y compararlos con un modelo de referencia simple.
5. Evaluar si el modelo anticipa la situación de 2025-2026 a partir de lo aprendido en años anteriores, e interpretar qué variables tienen más peso en la predicción.

## 5. Tipo de problema: clasificación binaria

Para cada división y cada mes, la variable objetivo vale 1 si la producción de esa división, tres meses después, es menor que la del mismo mes del año anterior (contracción interanual), y 0 si no lo es.

Es un problema de clasificación y no de regresión porque el modelo no predice cuánto va a producir la rama (un valor numérico), sino si va a estar en contracción o no (dos categorías).

La regla solo define la etiqueta. El modelo no aplica esa regla: en el mes de la predicción, la producción de tres meses después todavía no existe. Lo que el modelo aprende, a partir de los casos históricos ya observados, es la relación entre las condiciones económicas de un mes y el resultado de la rama tres meses más tarde.

En el total del período las clases están bastante equilibradas: en el 54% de los casos hubo caída interanual. Sin embargo, la proporción cambia mucho según el año: fue del 15% en 2021 y del 82% en 2024. Por eso, además de la exactitud, voy a analizar la precisión, el recall y el F1-score.

## 6. Datos y variables

Todas las fuentes son públicas y tienen frecuencia mensual. Los archivos ya están descargados.

| Variable | Descripción | Fuente |
|---|---|---|
| Producción por división (variable objetivo) | Índice de producción industrial manufacturero (IPI) de las 16 divisiones de la industria, enero de 2016 a agosto de 2026. | INDEC |
| Capacidad instalada | Utilización de la capacidad instalada: nivel general y 12 bloques sectoriales. A cada división se le asigna el bloque que le corresponde. | INDEC |
| Tipo de cambio | Tipo de cambio de referencia (Comunicación A 3500), promedio mensual. | BCRA |
| Tasa de interés | Tasas de interés de mercado (plazo fijo y préstamos). | BCRA |
| Importaciones | Importaciones mensuales totales, en millones de dólares. | INDEC |
| Evolución de la rama (complemento) | Variación interanual y mensual reciente de la división, evolución del nivel general de la industria y mes del año (estacionalidad). | INDEC |

Para cada variable externa se usa solo el último dato publicado en el mes de la predicción, para no incluir información del futuro. La base tiene 2.048 observaciones (16 divisiones × 128 meses). Al construir la variable objetivo y las variaciones interanuales quedan alrededor de 1.800 observaciones utilizables.

En un principio había previsto usar las importaciones separadas por uso económico (bienes de capital, insumos y bienes de consumo). Como no pude obtener esa serie, en esta etapa uso las importaciones totales, y la incorporaré si consigo los datos.

## 7. Modelos que podría utilizar

- **Modelo de referencia:** predecir que dentro de tres meses va a pasar lo mismo que hoy. Sirve para comprobar si el modelo aporta algo más que la tendencia actual.
- **Regresión Logística:** modelo base, simple e interpretable. A pesar de su nombre, es un modelo de clasificación: calcula la probabilidad de que la rama esté en contracción.
- **Árbol de Decisión:** permite visualizar las reglas que usa el modelo.
- **Random Forest y Gradient Boosting:** suelen tener mejor desempeño, captan relaciones no lineales y permiten analizar la importancia de las variables.
- **KNN:** como punto de comparación.

Para validar el modelo voy a respetar el orden temporal: entrenar con los datos hasta 2024 y evaluar con 2025-2026, para simular una situación real de predicción. Los hiperparámetros se ajustarán con validación cruzada temporal dentro del período de entrenamiento.

## 8. Limitaciones

- El modelo aprende de los patrones del pasado: si la situación actual tiene causas distintas a las de crisis anteriores, puede tener más dificultades para anticiparla.
- La pandemia de 2020 generó caídas atípicas que habrá que tratar con cuidado.
- Los bloques de capacidad instalada no coinciden uno a uno con las divisiones del IPI, por lo que algunas asignaciones son aproximadas.
- Los datos de los últimos meses son provisorios y pueden corregirse.

---

## 9. Actualizaciones posteriores a la entrega

El detalle está en [`02_descripcion_dataset_y_origen.md`](02_descripcion_dataset_y_origen.md) y al comienzo del notebook.

**Según la devolución de la Entrega 1:**
- Cada fila tiene un mes de decisión (cuando se publica el IPI) y un mes en que se conoce su resultado. En el entrenamiento solo entran filas cuyo resultado ya se conocía antes del corte.
- Los meses no se reparten entre entrenamiento y evaluación: las 16 divisiones de un mismo mes quedan siempre juntas.
- El modelo de referencia usa la última contracción publicada (`contraccion_hoy`).
- Las predicciones cuyo resultado todavía no se publicó quedan como pendientes.
- El objetivo específico 2 se reformuló (ver sección 4).

**Según la devolución de la Entrega 2:**
- **Horizonte.** El IPI de un mes *t* se publica en *t+2*, que es cuando se decide. Por eso "dentro de tres meses" se mide desde la decisión: el objetivo vale 1 si el IPI de *t+5* es menor que el de *t-7*. El resultado se conoce en *t+7*.
- **Proporción de clases con el horizonte definitivo.** Hay un 54,9% de contracción en las 1.728 filas modelables (abril 2017 a marzo 2026). La proporción va del 18% en 2021 al 94% en 2018.

**Variables que finalmente se usan:**
- **Tasa de interés:** BADLAR de bancos privados.
- **Balanza comercial:** se agregaron las exportaciones a las importaciones totales.
- **Mes del año:** no se incorporó como variable. Las variaciones interanuales reducen parte del efecto estacional, aunque no lo eliminan del todo.

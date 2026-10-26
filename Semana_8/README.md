# Semana 8

## Clase 8 — Aprendizaje no supervisado: segmentación de clientes con K-Means

**Objetivo:** identificar cuántos segmentos latentes de clientes existen a partir de su comportamiento de compra y uso del sitio, sin etiquetas previas.

### Estructura

```
Semana_8/
├── Datos/
│   └── dataset_segmentacion_clientes.csv
├── Notebooks/
│   └── clase8_kmeans_segmentacion.ipynb
└── README.md
```

### Resumen del trabajo

- **Dataset:** 700 clientes con frecuencia de compra, ticket promedio, tiempo en el sitio, sensibilidad a descuentos y tasa de devoluciones. Se excluyeron las columnas `noise_gauss` y `noise_uniform` por ser ruido.
- **Preprocesamiento:** estandarización con `StandardScaler`, porque las variables tienen escalas muy distintas.
- **Elección de k:** método del codo para k = 2 a 6 y coeficiente de silueta como apoyo. Se eligió **k = 6**.
- **Resultado:** seis segmentos, organizados en tres tipos de comprador (frecuente de ticket medio, esporádico premium y ocasional económico). Cada tipo se divide según la sensibilidad a descuentos o la tasa de devoluciones. Para cada segmento se propone una acción comercial.

### Cómo ejecutarlo

Abrir `Notebooks/clase8_kmeans_segmentacion.ipynb` en Jupyter y ejecutar todas las celdas. El notebook lee los datos desde `../Datos/`.

**Librerías:** pandas, numpy, matplotlib, scikit-learn.

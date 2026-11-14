"""Rutas y parámetros compartidos por todo el proyecto."""
from pathlib import Path

# Carpeta raíz del proyecto (Parcial/), así los scripts corren desde cualquier lugar
BASE = Path(__file__).resolve().parents[1]

DATA = BASE / "data"
RAW = DATA / "raw"
INTERIM = DATA / "interim"
PROCESSED = DATA / "processed"
EXTERNAL = DATA / "external"
MODELS = BASE / "models"
REPORTS = BASE / "reports"
FIGURES = REPORTS / "figures"

# Horizonte de predicción (devolución Entrega 2): el IPI de t se publica en t+2,
# que es cuando se decide; el objetivo es el mes t+5, 3 meses después.
REZAGO_PUBLICACION_IPI = 2
HORIZONTE = 5

PREDICTORAS = ["ipi_var_ia", "ipi_var_ia_lag1", "ipi_var_ia_lag2", "ipi_var_ia_cambio3m",
               "contraccion_hoy", "uci_bloque", "uci_bloque_dif_ia", "uci_general",
               "uci_general_dif_ia", "tc_var_ia", "tc_var_3m", "badlar", "badlar_dif_ia",
               "expo_var_ia", "impo_var_ia"]

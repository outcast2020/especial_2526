"""Configurações básicas do buscador de poemas."""
import os

DATA_PATH = os.getenv("POEMS_CSV_PATH", "data/poems.csv")

# quantis para tiers
Q_TOP = float(os.getenv("Q_TOP", "0.80"))
Q_BOTTOM = float(os.getenv("Q_BOTTOM", "0.20"))

# limite de candidatos internos antes de balancear
CANDIDATES_RHYME = int(os.getenv("CANDIDATES_RHYME", "80"))
CANDIDATES_THEME = int(os.getenv("CANDIDATES_THEME", "80"))

# modo balanceado padrão
N_EACH = int(os.getenv("N_EACH", "4"))

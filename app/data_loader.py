"""Funções de carregamento e validação do dataset de poemas."""
import pandas as pd

from .config import DATA_PATH


def load_df() -> pd.DataFrame:
    df = pd.read_csv(DATA_PATH)
    df["Content"] = df["Content"].astype(str)
    df["Author"] = df["Author"].astype(str)
    df["Title"] = df["Title"].astype(str)
    df["Views"] = pd.to_numeric(df["Views"], errors="coerce").fillna(0)
    df = df.dropna(subset=["Content"]).reset_index(drop=True)
    return df

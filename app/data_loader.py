"""Funções de carregamento e validação do dataset de poemas via KaggleHub."""
import os
import pandas as pd

import kagglehub
from kagglehub import KaggleDatasetAdapter

DATASET_ID = "oliveirasp6/poems-in-portuguese"

# Se você souber o nome do arquivo dentro do dataset, pode fixar aqui, ex: "poems.csv"
FILE_PATH = os.getenv("KAGGLE_FILE_PATH", "")  # opcional


def _list_files_in_dataset() -> list[str]:
    path = kagglehub.dataset_download(DATASET_ID)
    files = []
    for root, _, fs in os.walk(path):
        for f in fs:
            rel = os.path.relpath(os.path.join(root, f), path)
            files.append(rel)
    return sorted(files)


def load_df() -> pd.DataFrame:
    file_path = FILE_PATH

    # Auto-detect: se FILE_PATH vazio, tenta achar o 1º arquivo "tabular" do dataset
    if not file_path:
        files = _list_files_in_dataset()
        tabular = [f for f in files if f.lower().endswith((".csv", ".parquet"))]
        if len(tabular) == 0:
            raise FileNotFoundError(
                f"Não achei CSV/Parquet no dataset {DATASET_ID}. Arquivos disponíveis: {files[:50]}"
            )
        # se houver mais de um, pega o primeiro (pode ajustar manualmente via env KAGGLE_FILE_PATH)
        file_path = tabular[0]

    df = kagglehub.load_dataset(
        KaggleDatasetAdapter.PANDAS,
        DATASET_ID,
        file_path,
    )

    # valida/normaliza colunas
    expected = {"Author", "Title", "Content", "Views"}
    missing = expected - set(df.columns)
    if missing:
        raise KeyError(
            f"Dataset carregado de '{file_path}' não tem colunas esperadas. "
            f"Faltando: {sorted(missing)}. Colunas: {list(df.columns)}"
        )

    df["Content"] = df["Content"].astype(str)
    df["Author"] = df["Author"].astype(str)
    df["Title"] = df["Title"].astype(str)
    df["Views"] = pd.to_numeric(df["Views"], errors="coerce").fillna(0)

    df = df.dropna(subset=["Content"]).reset_index(drop=True)
    return df

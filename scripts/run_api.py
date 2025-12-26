"""Ponto de entrada executável para embutir a API em um binário Windows.

Este script pode ser empacotado com PyInstaller e depois instalado via
Inno Setup. Ele inicia o servidor Uvicorn usando a configuração padrão
(`POEMS_CSV_PATH` aponta para `data/poems.csv` empacotado no instalador).
"""
import os

import uvicorn


def main() -> None:
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run("app.api:app", host=host, port=port, reload=False)


if __name__ == "__main__":
    main()

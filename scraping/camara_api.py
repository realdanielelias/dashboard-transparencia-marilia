# RU4590111 Daniel Elias de Souza

import requests
import pandas as pd
import os
from config import DATA_DIR
from utils import rename_columns

BASE_URL = "https://cmmarilia.geosiap.net.br/portal-transparencia/api/default/execucao/detalhamento_despesas/detalhamento_despesas"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://cmmarilia.geosiap.net.br/portal-transparencia/execucao/detalhamento-despesas"
}

def fetch_despesas_ano(ano):
    """Coleta despesas da Câmara para um ano específico usando GET."""
    params = {
        "ano": ano,
        "id_entidade": 1,
        "dias": 0
    }

    response = requests.get(BASE_URL, params=params, headers=HEADERS)
    response.raise_for_status()

    data = response.json()

    # A API retorna um dicionário com chave "detalhamento_despesas"
    if "detalhamento_despesas" in data:
        return data["detalhamento_despesas"]

    return []


def scrape_camara_despesas_2020_2023():
    os.makedirs(DATA_DIR, exist_ok=True)

    all_rows = []

    for ano in range(2020, 2024):
        print(f"Coletando dados da Câmara para {ano}...")
        rows = fetch_despesas_ano(ano)

        for r in rows:
            r["ano"] = ano

        all_rows.extend(rows)

    df = pd.DataFrame(all_rows)

    # Renomeia colunas para português antes de salvar
    df = rename_columns(df, "camara")

    df.to_csv(f"{DATA_DIR}/camara_despesas_2020_2023.csv", index=False, encoding="utf-8")

    return df

import requests
import pandas as pd
import os
from config import DATA_DIR
from utils import rename_columns

URL = "https://transparencia.marilia.sp.gov.br/paiportalserver/modulovisao/filter"

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json;charset=utf-8",
    "Origin": "https://transparencia.marilia.sp.gov.br",
    "Referer": "https://transparencia.marilia.sp.gov.br/",
    "User-Agent": "Mozilla/5.0"
}

def get_dataset_type_from_visao(nome_visao):
    """Determina o tipo do dataset baseado no nome da visão"""
    if "covid" in nome_visao.lower():
        return "covid"
    elif "passagens" in nome_visao.lower():
        return "passagens"
    elif "investimentos" in nome_visao.lower():
        return "investimentos"
    elif "receita" in nome_visao.lower():
        return "receita"
    elif "emendas" in nome_visao.lower():
        return "emendas"
    else:
        return "unknown"

def scrape_visao(chave_modulo, nome_visao, periodicidade, anos, ordenacao, periodo=None):
    """
    Scraper universal para qualquer visão do portal da Prefeitura de Marília.
    Salva dados parciais mesmo em caso de erros.
    """

    all_data = []

    for ano in anos:
        print(f"Coletando {nome_visao} para {ano}...")

        pagina = 1
        max_retries = 3
        consecutive_errors = 0
        max_consecutive_errors = 5  # Máximo de erros consecutivos antes de parar

        while True:
            try:
                payload = {
                    "ChaveModulo": chave_modulo,
                    "NomeVisao": nome_visao,
                    "Filtros": [],
                    "Periodicidade": periodicidade,
                    "Periodo": periodo if periodicidade == "MENSAL" else None,
                    "Exercicio": ano,
                    "Pagina": pagina,
                    "QuantidadeRegistros": "100",
                    "Ordenacao": ordenacao,
                    "FiltroRedirecionaVisao": {
                        "Campo": None,
                        "Valor": None,
                        "TipoValor": None
                    }
                }

                response = requests.post(URL, json=payload, headers=HEADERS)
                
                # Tentar novamente em caso de erro 524 (temporário)
                if response.status_code == 524:
                    if consecutive_errors < max_retries:
                        print(f"Erro 524 na página {pagina}, tentando novamente ({consecutive_errors + 1}/{max_retries})...")
                        import time
                        time.sleep(3)  # Esperar 3 segundos
                        response = requests.post(URL, json=payload, headers=HEADERS)
                    else:
                        print(f"Erro 524 persistente na página {pagina}, pulando...")
                        pagina += 1
                        consecutive_errors = 0
                        continue
                
                response.raise_for_status()
                consecutive_errors = 0  # Reset contador de erros
                
                data = response.json()

                valores = data.get("Valores", [])
                total_paginas = data.get("QuantidadePaginas", 1)

                if not valores:
                    break

                for row in valores:
                    row["Ano"] = ano

                all_data.extend(valores)

                print(f"  Página {pagina}/{total_paginas}")

                if pagina >= total_paginas:
                    break

                pagina += 1

            except requests.exceptions.RequestException as e:
                consecutive_errors += 1
                print(f"Erro na página {pagina}: {e}")
                
                if consecutive_errors >= max_consecutive_errors:
                    print(f"Muitos erros consecutivos ({consecutive_errors}), salvando dados parciais...")
                    break
                
                pagina += 1
                import time
                time.sleep(2)  # Esperar antes de tentar próxima página
                continue

    # Salvar dados mesmo que parciais
    df = pd.DataFrame(all_data)

    # Renomeia colunas para português antes de salvar
    dataset_type = get_dataset_type_from_visao(nome_visao)
    df = rename_columns(df, dataset_type)

    os.makedirs(DATA_DIR, exist_ok=True)
    filename = f"{DATA_DIR}/{nome_visao}_dados.csv"
    df.to_csv(filename, index=False, encoding="utf-8")

    print(f"Arquivo salvo em: {filename} ({len(df)} linhas coletadas)")
    return df

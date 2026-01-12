# RU4590111 Daniel Elias de Souza

from scraping.universal_scraper import scrape_visao

def scrape_receita_analitica():
    """
    Coleta dados de Receita Analítica da Prefeitura de Marília.
    Versão limitada para teste - coleta apenas 2024-2025 para evitar timeouts.
    """
    return scrape_visao(
        chave_modulo="folha_pagamento_detalhes",
        nome_visao="ReceitaAnalitica",
        periodicidade="ANUAL",
        anos=[2024, 2025],  # Apenas anos recentes para teste
        ordenacao=[{"ColunaOrdem": "UnidadeGestora", "TipoOrdem": "ascend", "Ordem": 1}]
    )

def scrape_receita_analitica_completa():
    """
    Coleta dados completos de Receita Analítica (2020-2025).
    Use quando o servidor estiver mais estável.
    """
    return scrape_visao(
        chave_modulo="folha_pagamento_detalhes",
        nome_visao="ReceitaAnalitica",
        periodicidade="ANUAL",
        anos=[2020, 2021, 2022, 2023, 2024, 2025],
        ordenacao=[{"ColunaOrdem": "UnidadeGestora", "TipoOrdem": "ascend", "Ordem": 1}]
    )
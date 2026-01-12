from scraping.universal_scraper import scrape_visao

def scrape_emendas_parlamentares():
    """
    Coleta dados de Emendas Parlamentares da Prefeitura de Marília.
    """
    return scrape_visao(
        chave_modulo="emendas_parlamentares",
        nome_visao="EmendasParlamentares",
        periodicidade="ANUAL",
        anos=[2020, 2021, 2022, 2023, 2024, 2025],
        ordenacao=[{"ColunaOrdem": "NroEmpenho", "TipoOrdem": "ascend", "Ordem": 1}]
    )
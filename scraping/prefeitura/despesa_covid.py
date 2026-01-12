from scraping.universal_scraper import scrape_visao

def scrape_despesa_covid():
    return scrape_visao(
        chave_modulo="despesa_covid",
        nome_visao="despesacovid",
        periodicidade="ANUAL",
        anos=[2020, 2021, 2022, 2023, 2024, 2025],
        ordenacao=[{"ColunaOrdem": "NroEmpenho", "Ordem": 1}]
    )

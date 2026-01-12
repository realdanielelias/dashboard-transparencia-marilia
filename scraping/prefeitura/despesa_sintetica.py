from scraping.universal_scraper import scrape_visao

def scrape_despesa_sintetica():
    return scrape_visao(
        chave_modulo="despesa_sintetica",
        nome_visao="DespesaSintetica",
        periodicidade="ANUAL",
        anos=[2020, 2021, 2022, 2023, 2024, 2025],
        ordenacao=[{"ColunaOrdem": "NaturezaDespesa", "Ordem": 1}]
    )

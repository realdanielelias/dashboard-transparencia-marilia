from scraping.universal_scraper import scrape_visao

def scrape_investimentos(periodo="JANEIRO"):
    return scrape_visao(
        chave_modulo="DespesaAgrupada",
        nome_visao="DespesaseInvestimentos",
        periodicidade="MENSAL",
        periodo=periodo,
        anos=[2024, 2025, 2026],
        ordenacao=[{"ColunaOrdem": "NroEmpenho", "Ordem": 1}]
    )

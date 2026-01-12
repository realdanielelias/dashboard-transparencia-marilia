from scraping.camara_api import scrape_camara_despesas_2020_2023

# Scrapers da Prefeitura (cada um chama o universal_scraper)
from scraping.prefeitura.despesa_covid import scrape_despesa_covid
from scraping.prefeitura.passagens import scrape_passagens
from scraping.prefeitura.investimentos import scrape_investimentos
from scraping.prefeitura.receita_analitica import scrape_receita_analitica
from scraping.prefeitura.emendas_parlamentares import scrape_emendas_parlamentares

print("Iniciando scraping...\n")

# Câmara Municipal
try:
    scrape_camara_despesas_2020_2023()
    print("Câmara Municipal (2020–2023): OK")
except Exception as e:
    print("Erro na Câmara:", e)

# Receita Analítica (versão limitada para evitar timeouts)
try:
    scrape_receita_analitica()
    print("Prefeitura - Receita Analítica: OK")
except Exception as e:
    print("Erro:", e)

# Emendas Parlamentares
try:
    scrape_emendas_parlamentares()
    print("Prefeitura - Emendas Parlamentares: OK")
except Exception as e:
    print("Erro:", e)

# Prefeitura – Covid
try:
    scrape_despesa_covid()
    print("Prefeitura - Despesas Covid: OK")
except Exception as e:
    print("Erro:", e)

# Prefeitura – Passagens e Locomoção
try:
    scrape_passagens()
    print("Prefeitura - Passagens e Locomoção: OK")
except Exception as e:
    print("Erro:", e)

# Prefeitura – Investimentos (mensal)
try:
    scrape_investimentos(periodo="JANEIRO")
    print("Prefeitura - Investimentos (Janeiro): OK")
except Exception as e:
    print("Erro:", e)

print("\nScraping finalizado.")

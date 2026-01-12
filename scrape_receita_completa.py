#!/usr/bin/env python3
"""
Script para executar scraping completo da Receita Analítica.
Use quando o servidor estiver mais estável.
"""

from scraping.prefeitura.receita_analitica import scrape_receita_analitica_completa

if __name__ == "__main__":
    print("Iniciando scraping COMPLETO da Receita Analítica (2020-2025)...")
    print("Isso pode levar muito tempo devido ao grande volume de dados.")
    print("Pressione Ctrl+C para interromper e salvar dados parciais.\n")

    try:
        result = scrape_receita_analitica_completa()
        print(f"\n✅ Scraping concluído! {len(result)} registros coletados.")
    except KeyboardInterrupt:
        print("\n⚠️  Scraping interrompido pelo usuário. Dados parciais foram salvos.")
    except Exception as e:
        print(f"\n❌ Erro durante scraping: {e}")
        print("Dados parciais podem ter sido salvos.")
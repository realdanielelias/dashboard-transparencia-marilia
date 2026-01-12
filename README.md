# RU4590111 Daniel Elias de Souza

# Dashboard de Transparência Municipal - Marília/SP

Dashboard interativo para análise de dados de transparência pública da Câmara Municipal e Prefeitura de Marília/SP.

Esse projeto foi desenvolvido como trabalho para o curso de Desenvolvimento e Analise de Sistemas da Uninter, na disciplina "Atividade Extensionista II: Tecnologia Aplicada a Inclusao Digital".
 
Por se tratar de um projeto inicial para estudo, ha algumas limitacoes e talvez existam algumas imprecisoes no tratamento dos dados. No futuro, esse projeto sera expandido fora das atividades curriculares de forma pessoal.

## Funcionalidades

- 📊 Visualizações interativas (barras, pizza, distribuições, correlações)
- 🔍 Consultas SQL diretas nos dados
- 📥 Exportação de dados filtrados
- 🌐 Interface em português
- 📈 Análises estatísticas automáticas

## Conjuntos de Dados

- Câmara Municipal: Despesas (2020-2023)
- Prefeitura: COVID-19, Passagens, Investimentos, Receita Analítica, Emendas Parlamentares

## 📊 Como Usar

1. Selecione um conjunto de dados no menu lateral
2. Use os filtros para refinar os dados
3. Explore as diferentes abas de visualização:
   - **Barras**: Gráficos de barras interativos
   - **Pizza**: Distribuição percentual
   - **Distribuição**: Histogramas e estatísticas
   - **Correlação**: Relacionamentos entre variáveis
   - **Temporal**: Análises ao longo do tempo
   - **SQL**: Consultas diretas nos dados

## 🛠️ Desenvolvimento Local

Se quiser executar localmente para desenvolvimento:

### Pré-requisitos
- Python 3.8+
- Git

### Instalação

1. Clone o repositório:
```bash
git clone https://github.com/SEU_USERNAME/dashboard-transparencia-marilia.git
cd dashboard-transparencia-marilia
```

2. Crie um ambiente virtual:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# ou
.venv\Scripts\activate     # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

4. Execute o scraping dos dados (opcional):
```bash
# esse repositorio ja contem alguns dados baixados, mas caso queria testar o scrapping ou obter dados mais atualizados, delete os arquivos no /data e rode o comando abaixo:

python run_scraping.py
```

5. Execute o dashboard:
```bash
streamlit run dashboard/app.py
```

## 📁 Estrutura do Projeto

```
dashboard/
├── dashboard/app.py          # Aplicação principal Streamlit
├── scraping/                 # Scripts de coleta de dados
├── data/                     # Dados coletados (CSV)
├── utils.py                  # Funções utilitárias
├── requirements.txt          # Dependências Python
├── run_scraping.py          # Script para executar todos os scrapers
└── README.md                 # Este arquivo
```
## 📄 Licença

Este projeto é open source e pode ser usado livremente para fins educacionais e de transparência pública.

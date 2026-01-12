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

## 🚀 Implantação no Streamlit Cloud

### Pré-requisitos
- Conta GitHub (gratuita)
- Conta Streamlit Cloud (gratuita)

### Passos para Deploy

1. **Crie um repositório no GitHub:**
   - Acesse [github.com](https://github.com)
   - Clique em "New repository"
   - Nome: `dashboard-transparencia-marilia`
   - Descrição: "Dashboard interativo de transparência municipal Marília/SP"
   - Deixe **público**
   - **Não** marque "Add a README file"

2. **Faça upload do código:**
   ```bash
   # No terminal, navegue até a pasta do projeto
   cd /caminho/para/dashboard

   # Adicione o repositório remoto (substitua SEU_USERNAME)
   git remote add origin https://github.com/SEU_USERNAME/dashboard-transparencia-marilia.git

   # Faça push do código
   git push -u origin main
   ```

3. **Implante no Streamlit Cloud:**
   - Acesse [share.streamlit.io](https://share.streamlit.io)
   - Conecte sua conta GitHub
   - Selecione o repositório `dashboard-transparencia-marilia`
   - Arquivo principal: `dashboard/app.py`
   - Clique em "Deploy"

### 🎯 Resultado

Após o deploy, seu dashboard ficará disponível em uma URL como:
```
https://dashboard-transparencia-marilia.streamlit.app
```

Qualquer pessoa poderá acessar o dashboard através de um navegador, sem precisar instalar nada!

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

## 📈 Limitações do Streamlit Cloud

- Até 1GB de dados
- Até 1000 horas de uso por mês (gratuito)
- Dados públicos apenas

## 🤝 Contribuição

Para contribuir com melhorias:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-feature`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova feature'`)
4. Push para a branch (`git push origin feature/nova-feature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto é open source e pode ser usado livremente para fins educacionais e de transparência pública.

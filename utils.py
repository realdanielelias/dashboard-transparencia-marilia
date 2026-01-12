# RU4590111 Daniel Elias de Souza

# Funções utilitárias para processamento de dados
import pandas as pd
import re

def convert_brazilian_currency(value):
    """Converte valor monetário brasileiro (string) para float"""
    if pd.isna(value) or value == '':
        return None

    # Converte para string se não for
    value_str = str(value).strip()

    # Remove símbolos de moeda e espaços
    value_str = re.sub(r'[R$\s]', '', value_str)

    # Trata casos especiais
    if value_str in ['-', 'N/A', 'null', 'None']:
        return None

    try:
        # Remove pontos (separadores de milhares) e substitui vírgula por ponto
        value_str = value_str.replace('.', '').replace(',', '.')
        return float(value_str)
    except (ValueError, AttributeError):
        return None

def convert_numeric_columns(df):
    """Converte colunas que parecem conter valores numéricos"""
    df_converted = df.copy()

    # Colunas que provavelmente contêm valores monetários
    monetary_keywords = ['valor', 'vl_', 'preço', 'custo', 'total', 'saldo', 'arrecadado', 'previsto']

    for col in df_converted.columns:
        # Verifica se é uma coluna de texto
        if df_converted[col].dtype == 'object':
            col_lower = col.lower()

            # Verifica se o nome da coluna sugere valor monetário
            if any(keyword in col_lower for keyword in monetary_keywords):
                # Tenta converter os valores
                converted_values = []
                for val in df_converted[col]:
                    converted = convert_brazilian_currency(val)
                    converted_values.append(converted)

                # Se conseguiu converter pelo menos 80% dos valores, converte a coluna
                valid_conversions = sum(1 for v in converted_values if v is not None)
                if valid_conversions / len(converted_values) > 0.8:
                    df_converted[col] = converted_values
                    df_converted[col] = pd.to_numeric(df_converted[col], errors='coerce')

    return df_converted

def rename_columns(df, dataset_type):
    """Renomeia colunas para português mais compreensível"""
    if dataset_type == "camara":
        column_mapping = {
            'natureza': 'Natureza da Despesa',
            'elemento': 'Elemento',
            'vl_previsto': 'Valor Previsto',
            'vl_total_emp': 'Total Empenhado',
            'vl_total_liq': 'Total Liquidado',
            'vl_total_pag': 'Total Pago',
            'vl_jan_emp': 'Jan Empenhado',
            'vl_fev_emp': 'Fev Empenhado',
            'vl_mar_emp': 'Mar Empenhado',
            'vl_abr_emp': 'Abr Empenhado',
            'vl_mai_emp': 'Mai Empenhado',
            'vl_jun_emp': 'Jun Empenhado',
            'vl_jul_emp': 'Jul Empenhado',
            'vl_ago_emp': 'Ago Empenhado',
            'vl_set_emp': 'Set Empenhado',
            'vl_out_emp': 'Out Empenhado',
            'vl_nov_emp': 'Nov Empenhado',
            'vl_dez_emp': 'Dez Empenhado',
            'vl_jan_liq': 'Jan Liquidado',
            'vl_fev_liq': 'Fev Liquidado',
            'vl_mar_liq': 'Mar Liquidado',
            'vl_abr_liq': 'Abr Liquidado',
            'vl_mai_liq': 'Mai Liquidado',
            'vl_jun_liq': 'Jun Liquidado',
            'vl_jul_liq': 'Jul Liquidado',
            'vl_ago_liq': 'Ago Liquidado',
            'vl_set_liq': 'Set Liquidado',
            'vl_out_liq': 'Out Liquidado',
            'vl_nov_liq': 'Nov Liquidado',
            'vl_dez_liq': 'Dez Liquidado',
            'vl_jan_pag': 'Jan Pago',
            'vl_fev_pag': 'Fev Pago',
            'vl_mar_pag': 'Mar Pago',
            'vl_abr_pag': 'Abr Pago',
            'vl_mai_pag': 'Mai Pago',
            'vl_jun_pag': 'Jun Pago',
            'vl_jul_pag': 'Jul Pago',
            'vl_ago_pag': 'Ago Pago',
            'vl_set_pag': 'Set Pago',
            'vl_out_pag': 'Out Pago',
            'vl_nov_pag': 'Nov Pago',
            'vl_dez_pag': 'Dez Pago',
            'ano': 'Ano'
        }
    elif dataset_type in ["covid", "passagens", "investimentos", "receita", "emendas"]:
        column_mapping = {
            'NroEmpenho': 'Número do Empenho',
            'UG': 'Unidade Gestora',
            'Modalidade': 'Modalidade',
            'NomeFornecedor': 'Nome do Fornecedor',
            'DataEmp': 'Data do Empenho',
            'ValorEmpenhado': 'Valor Empenhado',
            'ValorLiquidado': 'Valor Liquidado',
            'ValorPago': 'Valor Pago',
            'Programa': 'Programa',
            'UnidadeOrcamentaria': 'Unidade Orçamentária',
            'ID': 'ID',
            'Id': 'ID Secundário',
            'Ano': 'Ano',
            'DataMovEmp': 'Data do Movimento',
            'TipEmpenho': 'Tipo de Empenho',
            'CNPJ': 'CNPJ',
            'Evento': 'Evento',
            'Vinculo': 'Vínculo',
            'FonteRecurso': 'Fonte de Recurso',
            'Categoria': 'Categoria',
            'Elemento': 'Elemento',
            'BemouServico': 'Bem ou Serviço',
            'Itens': 'Itens',
            'Liquidacoes': 'Liquidações',
            'Documentos': 'Documentos',
            'Pagamentos': 'Pagamentos',
            # Campos específicos para Receita Analítica
            'UnidadeGestora': 'Unidade Gestora',
            'FonteRecursos': 'Fonte de Recursos',
            'NaturezaReceita': 'Natureza da Receita',
            'ValorArrecadado': 'Valor Arrecadado',
            'ValorPrevisto': 'Valor Previsto',
            'PercentualArrecadacao': 'Percentual de Arrecadação',
            # Campos específicos para Emendas Parlamentares
            'Parlamentar': 'Parlamentar',
            'Partido': 'Partido',
            'Emenda': 'Número da Emenda',
            'ValorEmenda': 'Valor da Emenda',
            'Localidade': 'Localidade',
            'Objetivo': 'Objetivo',
            'StatusEmenda': 'Status da Emenda'
        }
    else:
        return df  # Retorna sem alterações se não reconhecido

    # Aplica o mapeamento apenas para colunas que existem
    df_renamed = df.rename(columns={k: v for k, v in column_mapping.items() if k in df.columns})
    return df_renamed
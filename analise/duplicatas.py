import pandas as pd

# Lista de arquivos CSV que contêm suas tabelas
arquivos_csv = ['./agencias.csv', './clientes.csv', './colaborador_agencia.csv', './propostas_credito.csv','./transacoes.csv', './colaboradores.csv']

for arquivo in arquivos_csv:
    # Carregar a tabela
    tabela = pd.read_csv(arquivo)
    
    # Identificar e contar duplicatas
    num_duplicadas = tabela.duplicated().sum()
    num_colunas_nulas = tabela.isna().sum()
    
    print(f"{arquivo} tem {num_duplicadas} linhas duplicadas.")
    print(f"{arquivo} tem {num_colunas_nulas} colunas com valores nulos.")

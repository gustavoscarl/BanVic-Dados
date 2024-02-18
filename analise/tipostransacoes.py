import pandas as pd

# Carregar os dados do arquivo "transacoes.csv"
transacoes_df = pd.read_csv('./transacoes.csv')

# Encontrando os tipos únicos de "nome_transacao"
tipos_transacoes_unicos = transacoes_df['nome_transacao'].unique()

print(tipos_transacoes_unicos)
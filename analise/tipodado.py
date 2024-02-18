import pandas as pd

# Carregar o arquivo transacoes.csv
transacoes = pd.read_csv('./transacoes.csv')

# Verificar o tipo de dado da coluna 'data_transacao'
tipo_dado = transacoes['data_transacao'].dtype

print("Tipo de dado da coluna 'data_transacao':", tipo_dado)
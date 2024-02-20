import pandas as pd
import matplotlib.pyplot as plt

# Exemplo de carregamento dos dados
transacoes = pd.read_csv('./transacoes.csv')

# Extrair apenas a data (YYYY-MM-DD) da coluna 'data_transacao'
transacoes['data_simples'] = transacoes['data_transacao'].str[:10]

# Filtrar transações que não contêm "Pix" no nome
transacoes_sem_pix = transacoes[~transacoes['nome_transacao'].str.contains("Pix")]

# Dividir transações em antes e em/depois de 25 de dezembro de 2020, usando 'data_simples'
transacoes_antes = transacoes_sem_pix[transacoes_sem_pix['data_simples'] < '2020-12-25']
transacoes_depois = transacoes_sem_pix[transacoes_sem_pix['data_simples'] >= '2020-12-25']

# Contar transações
num_transacoes_antes = len(transacoes_antes)
num_transacoes_depois = len(transacoes_depois)

# Dados para plotagem
categorias = ['Antes de 25/12/2020', 'Em/Depois de 25/12/2020']
valores = [num_transacoes_antes, num_transacoes_depois]

# Contar transações
num_transacoes_antes = len(transacoes_antes)
num_transacoes_depois = len(transacoes_depois)

# Dados para plotagem
categorias = ['Antes de 25/12/2020', 'Em/Depois de 25/12/2020']
valores = [num_transacoes_antes, num_transacoes_depois]

# Plotagem
plt.figure(figsize=(10, 6))
bars = plt.bar(categorias, valores, color=['blue', 'orange'])
plt.title('Número de Transações Excluindo Pix Antes e Em/Depois de 25/12/2020')
plt.ylabel('Número de Transações')

# Adicionando o número total de transações em cada barra
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2.0, yval, int(yval), va='bottom', ha='center')

plt.show()

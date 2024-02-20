import pandas as pd
import matplotlib.pyplot as plt

clientes = pd.read_csv('./clientes.csv')
transacoes = pd.read_csv('./transacoes.csv')

# Pegar os primeiros 10 dígitos da string e converter para formato de data
transacoes['data_simples'] = pd.to_datetime(transacoes['data_transacao'].str[:10])

clientes['data_inclusao_simples'] = pd.to_datetime(clientes['data_inclusao'].str[:10])

# Definir a data de divisão
data_divisao = pd.to_datetime('2020-12-25')

# Filtrar transações excluindo "Pix" (supondo que 'nome_transacao' seja a coluna relevante)
transacoes_sem_pix = transacoes[~transacoes['nome_transacao'].str.contains("Pix")]

# Filtrar transações antes e depois da data de divisão
transacoes_antes = transacoes_sem_pix[transacoes_sem_pix['data_simples'] < data_divisao]
transacoes_depois = transacoes_sem_pix[transacoes_sem_pix['data_simples'] >= data_divisao]

# Calculando o total de clientes antes e depois da data de divisão baseado na 'data_inclusao'
clientes_antes = clientes[clientes['data_inclusao_simples'] < data_divisao]
clientes_depois = clientes[clientes['data_inclusao_simples'] >= data_divisao]

# Calculate the total number of transactions for each period
total_transacoes_antes = len(transacoes_sem_pix[transacoes_sem_pix['data_simples'] < data_divisao])
total_transacoes_depois = len(transacoes_sem_pix[transacoes_sem_pix['data_simples'] >= data_divisao])

# Calculate the average number of transactions per client for each period
media_transacoes_antes = total_transacoes_antes / len(clientes_antes)
media_transacoes_depois = total_transacoes_depois / len(clientes)

# Plotting
plt.figure(figsize=(8, 5))
bars = plt.bar(['Antes de 25/12/2020', 'Depois de 25/12/2020'], [media_transacoes_antes, media_transacoes_depois], color=['blue', 'orange'])
plt.title('Média de Transações por Cliente Excluindo Pix')
plt.ylabel('Média de Transações por Cliente')

# Adding the total number of transactions on each bar
for bar, total in zip(bars, [media_transacoes_antes, media_transacoes_depois]):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{int(total)}', ha='center', va='bottom')

plt.show()

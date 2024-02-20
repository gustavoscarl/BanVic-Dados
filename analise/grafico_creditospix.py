import pandas as pd
import matplotlib.pyplot as plt
import numpy as np  # Para usar np.abs() e obter o valor absoluto

# Carregar os dados
clientes = pd.read_csv('./clientes.csv')
transacoes = pd.read_csv('./transacoes.csv')

# Converter as datas para datetime
transacoes['data_simples'] = pd.to_datetime(transacoes['data_transacao'].str[:10])
clientes['data_inclusao_simples'] = pd.to_datetime(clientes['data_inclusao'].str[:10])

# Definir a data de divisão
data_divisao = pd.to_datetime('2020-12-25')

# Filtrar transações que contenham "Crédito" e converter o valor para absoluto
transacoes_credito = transacoes[transacoes['nome_transacao'].str.contains("Crédito")]
transacoes_credito['valor_absoluto'] = np.abs(transacoes_credito['valor_transacao'])

# Filtrar transações de crédito antes e depois da data de divisão
transacoes_credito_antes = transacoes_credito[transacoes_credito['data_simples'] < data_divisao]
transacoes_credito_depois = transacoes_credito[transacoes_credito['data_simples'] >= data_divisao]

clientes_antes = clientes[clientes['data_inclusao_simples'] < data_divisao]
clientes_depois = clientes[clientes['data_inclusao_simples'] >= data_divisao]

# Calcular o valor total de crédito para cada período
valor_total_credito_antes = transacoes_credito_antes['valor_absoluto'].sum()
valor_total_credito_depois = transacoes_credito['valor_absoluto'].sum()

# Calcular a média do valor de crédito por cliente para cada período
media_valor_credito_antes = valor_total_credito_antes / len(clientes_antes)
media_valor_credito_depois = valor_total_credito_depois / len(clientes)

# Plotar o gráfico
plt.figure(figsize=(8, 5))
bars = plt.bar(['Antes de 25/12/2020', 'Depois de 25/12/2020'], [media_valor_credito_antes, media_valor_credito_depois], color=['blue', 'orange'])
plt.title('Média de Valor de Crédito por Cliente')
plt.ylabel('Média de Valor de Crédito')

# Adicionando o valor total de crédito em cada barra
for bar, total in zip(bars, [media_valor_credito_antes, media_valor_credito_depois]):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2.0, height, f'{int(total)}', ha='center', va='bottom')

plt.show()

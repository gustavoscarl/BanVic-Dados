import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Carregar os dados
transacoes = pd.read_csv('transacoes.csv')

# Converter 'data_transacao' para datetime
transacoes['data_transacao'] = pd.to_datetime(transacoes['data_transacao'].str[:10])
# Agrupar por 'num_conta' e calcular a diferença de dias entre transações
transacoes = transacoes.sort_values(by=['num_conta', 'data_transacao'])
transacoes['diferenca_dias'] = transacoes.groupby('num_conta')['data_transacao'].diff().dt.days

# Agora, vamos encontrar a maior diferença de dias para cada cliente
maior_diferenca_dias = transacoes.groupby('num_conta')['diferenca_dias'].max().reset_index()

# Para simplificar, vamos assumir que você deseja criar faixas de 30 dias
bins = [0, 30, 60, 90, 120, 150, float('inf')]
labels = ['0-29', '30-59', '60-89', '90-119', '120-149', '150+']
maior_diferenca_dias['faixa_inatividade'] = pd.cut(maior_diferenca_dias['diferenca_dias'], bins=bins, labels=labels)

# Agora você pode calcular a porcentagem de clientes em cada faixa de inatividade
porcentagem_por_faixa = (maior_diferenca_dias['faixa_inatividade'].value_counts(normalize=True) * 100).sort_index()

# E finalmente, plotar o gráfico de barras
porcentagem_por_faixa.plot(kind='bar')
plt.title('Distribuição de Inatividade entre Transações')
plt.xlabel('Faixas de Dias de Inatividade')
plt.ylabel('Porcentagem de Clientes (%)')
plt.show()

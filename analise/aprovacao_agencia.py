import pandas as pd
import matplotlib.pyplot as plt


# Carregar os dados
transacoes = pd.read_csv('./transacoes.csv')
contas = pd.read_csv('./contas.csv')
# Supondo que exista um arquivo para agências, caso contrário, ajuste conforme necessário
agencias = pd.read_csv('./agencias.csv')

# Desconsiderar a agência 10 de todas as operações
# Para contas
contas = contas[contas['cod_agencia'] != 10]

# Para transações, você precisa primeiro garantir que cada transação esteja ligada à sua respectiva agência
# Isso é feito associando transações com contas pelo 'num_conta'
transacoes_agencias = pd.merge(transacoes, contas[['num_conta', 'cod_agencia']], on='num_conta')

# Agora, você pode aplicar o filtro para desconsiderar transações da agência 10
transacoes_agencias = transacoes_agencias[transacoes_agencias['cod_agencia'] != 10]

# Se você também quiser aplicar o filtro diretamente nas agências
# Este passo é opcional, dependendo se você precisa trabalhar diretamente com os dados das agências
agencias = agencias[agencias['cod_agencia'] != 10]

# Filtrar transações que contêm "Crédito"
transacoes_credito = transacoes[transacoes['nome_transacao'].str.contains('Crédito', na=False)]

# Associar transações a contas para obter a agência de cada transação
transacoes_agencias = pd.merge(transacoes_credito, contas[['num_conta', 'cod_agencia']], left_on='num_conta', right_on='num_conta')

# Calcular o total de transações de crédito por agência
total_transacoes_por_agencia = transacoes_agencias.groupby('cod_agencia').size().reset_index(name='total_transacoes')

# Calcular o total de clientes por agência
total_clientes_por_agencia = contas['cod_agencia'].value_counts().reset_index()
total_clientes_por_agencia.columns = ['cod_agencia', 'total_clientes']

# Juntar os dois DataFrames
dados_agencia = pd.merge(total_transacoes_por_agencia, total_clientes_por_agencia, on='cod_agencia')

# Calcular a média de transações de crédito por cliente por agência
dados_agencia['media_transacoes_por_cliente'] = dados_agencia['total_transacoes'] / dados_agencia['total_clientes']

# Ordenando os dados para melhor visualização no gráfico
dados_agencia.sort_values('media_transacoes_por_cliente', ascending=False, inplace=True)

# Criando o gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(dados_agencia['cod_agencia'].astype(str), dados_agencia['media_transacoes_por_cliente'], color='skyblue')
plt.title('Média de Transações de Crédito por Cliente por Agência')
plt.xlabel('Código da Agência')
plt.ylabel('Média de Transações de Crédito por Cliente')
plt.xticks(rotation=45)
plt.show()

import pandas as pd
import matplotlib.pyplot as plt



# Carregar os dados
clientes = pd.read_csv('clientes.csv')
transacoes = pd.read_csv('transacoes.csv')
contas = pd.read_csv('contas.csv')

# Preparação dos dados dos clientes
clientes['ano_nascimento'] = clientes['data_nascimento'].str[:4].astype(int)
clientes['idade'] = 2024 - clientes['ano_nascimento']

# Definir faixas etárias
bins = [18, 25, 33, 40, 50, float('inf')]
labels = ['18-25', '26-33', '34-40', '41-50', '50+']
clientes['faixa_etaria'] = pd.cut(clientes['idade'], bins=bins, labels=labels, right=False)

# Filtrar transações excluindo Pix
transacoes_filtradas = transacoes[~transacoes['nome_transacao'].isin(['Pix - Recebido', 'Pix - Realizado'])]

# Associar transações a contas
transacoes_contas = pd.merge(transacoes_filtradas, contas, on='num_conta')

# Associar contas a clientes para obter a faixa etária
transacoes_clientes = pd.merge(transacoes_contas, clientes[['cod_cliente', 'faixa_etaria']], on='cod_cliente')

# Contar transações por cliente e faixa etária
transacoes_por_cliente = transacoes_clientes.groupby(['cod_cliente', 'faixa_etaria']).size().reset_index(name='num_transacoes')

# Calcular o total de transações por faixa etária
total_transacoes_faixa = transacoes_clientes.groupby('faixa_etaria').size().reset_index(name='total_transacoes')

# Calcular o total de clientes por faixa etária
total_clientes_faixa = clientes['faixa_etaria'].value_counts().reset_index()
total_clientes_faixa.columns = ['faixa_etaria', 'total_clientes']

# Juntar os dois DataFrames
total_transacoes_clientes_faixa = pd.merge(total_transacoes_faixa, total_clientes_faixa, on='faixa_etaria')

# Calcular a média do número de transações por total de clientes em cada faixa etária
total_transacoes_clientes_faixa['media_transacoes_por_cliente'] = total_transacoes_clientes_faixa['total_transacoes'] / total_transacoes_clientes_faixa['total_clientes']

print(total_transacoes_clientes_faixa[['faixa_etaria', 'total_clientes', 'media_transacoes_por_cliente']])

# Certifique-se de que 'total_transacoes_clientes_faixa' é o DataFrame final obtido no passo anterior
# Plotando o gráfico de barras

plt.figure(figsize=(10, 6))  # Configura o tamanho do gráfico
plt.bar(total_transacoes_clientes_faixa['faixa_etaria'], total_transacoes_clientes_faixa['media_transacoes_por_cliente'], color='skyblue')

plt.title('Média do Número de Transações por Cliente em Cada Faixa Etária')  # Título do gráfico
plt.xlabel('Faixa Etária')  # Rótulo do eixo X
plt.ylabel('Média de Transações por Cliente')  # Rótulo do eixo Y
plt.xticks(rotation=45)  # Rotação dos rótulos do eixo X para melhor visualização

plt.show()  # Exibe o gráfico

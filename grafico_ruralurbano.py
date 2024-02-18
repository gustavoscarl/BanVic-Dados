import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados do arquivo "clientes.csv" e "propostas_credito.csv"
clientes_df = pd.read_csv('./clientes.csv')
propostas_df = pd.read_csv('./propostas_credito.csv')

# Determinando se o cliente é urbano ou rural baseado no endereço
clientes_df['tipo_cliente'] = clientes_df['endereco'].str.contains('Fazenda|Sítio|Chácara').apply(lambda x: 'Rural' if x else 'Urbano')

# Combinando os dados dos clientes com as propostas aprovadas
dados_combinados = pd.merge(clientes_df, propostas_df[propostas_df['status_proposta'] == 'Aprovada'], on='cod_cliente')

# Calculando o total de financiamento aprovado por tipo de cliente
financiamento_por_tipo = dados_combinados.groupby('tipo_cliente')['valor_financiamento'].sum()

# Calculando o número total de clientes por tipo
clientes_por_tipo = clientes_df['tipo_cliente'].value_counts()

# Calculando a média de financiamento aprovado por cliente por tipo
media_financiamento_por_tipo = financiamento_por_tipo / clientes_por_tipo

# Plotando o gráfico de barras horizontais
media_financiamento_por_tipo.plot(kind='barh', color=['blue', 'green'])
plt.title('Média de Financiamento Aprovado por Cliente Urbano vs Rural')
plt.xlabel('Média de Financiamento Aprovado')
plt.ylabel('Tipo de Cliente')
plt.tight_layout()
plt.show()

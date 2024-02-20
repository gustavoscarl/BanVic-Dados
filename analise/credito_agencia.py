import pandas as pd
import matplotlib.pyplot as plt

# Suponha que os DataFrames já estão carregados
propostas_credito = pd.read_csv('./propostas_credito.csv')
contas = pd.read_csv('./contas.csv')

# Filtrar propostas de crédito com status "Aprovada"
propostas_aprovadas = propostas_credito[propostas_credito['status_proposta'] == 'Aprovada']

# Contar o número de propostas aprovadas por cliente
propostas_por_cliente = propostas_aprovadas.groupby('cod_cliente').size().reset_index(name='num_propostas')

# Associar cada proposta aprovada à sua respectiva agência
propostas_agencia = pd.merge(propostas_por_cliente, contas[['cod_cliente', 'cod_agencia']], on='cod_cliente')

# Contar o número total de propostas aprovadas por agência
propostas_por_agencia = propostas_agencia.groupby('cod_agencia')['num_propostas'].sum().reset_index()

# Contar o número total de clientes por agência
clientes_por_agencia = contas.groupby('cod_agencia').size().reset_index(name='total_clientes')

# Juntar as contagens de propostas aprovadas e total de clientes por agência
dados_agencia = pd.merge(propostas_por_agencia, clientes_por_agencia, on='cod_agencia')

# Calcular a razão de propostas aprovadas por total de clientes para cada agência
dados_agencia['razao_propostas_cliente'] = dados_agencia['num_propostas'] / dados_agencia['total_clientes']

# Ordenar dados para visualização
dados_agencia.sort_values('razao_propostas_cliente', ascending=False, inplace=True)

# Criar o gráfico
plt.figure(figsize=(10, 6))
plt.bar(dados_agencia['cod_agencia'].astype(str), dados_agencia['razao_propostas_cliente'], color='skyblue')
plt.title('Razão de Propostas de Crédito Aprovadas por Total de Clientes por Agência')
plt.xlabel('Código da Agência')
plt.ylabel('Razão de Propostas Aprovadas por Cliente')
plt.xticks(rotation=45)
plt.show()

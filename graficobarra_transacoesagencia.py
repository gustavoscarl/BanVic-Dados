import pandas as pd
import matplotlib.pyplot as plt

# Load the data
propostas_df = pd.read_csv('./propostas_credito.csv')
contas_df = pd.read_csv('./contas.csv')

# Filter for approved proposals
aprovadas_df = propostas_df[propostas_df['status_proposta'] == 'Aprovada']

# Merge with contas_df to get agency codes
merged_df = aprovadas_df.merge(contas_df[['cod_cliente', 'cod_agencia']], on='cod_cliente')

# Group by agency and sum financing values
financiamento_por_agencia = merged_df.groupby('cod_agencia')['valor_financiamento'].sum().reset_index()

# Count the total number of clients per agency
clientes_por_agencia = contas_df['cod_agencia'].value_counts().reset_index()
clientes_por_agencia.columns = ['cod_agencia', 'total_clientes']

# Merge the financing sum with the client count
financiamento_clientes_agencia = financiamento_por_agencia.merge(clientes_por_agencia, on='cod_agencia')

# Calculate the ratio
financiamento_clientes_agencia['ratio'] = financiamento_clientes_agencia['valor_financiamento'] / financiamento_clientes_agencia['total_clientes']





# Plotting the ratio
plt.figure(figsize=(10, 6))
plt.bar(financiamento_clientes_agencia['cod_agencia'].astype(str), financiamento_clientes_agencia['ratio'], color='skyblue')
plt.title('Razão de Financiamento Aprovado por Clientes por cada Agência')
plt.xlabel('Código da Agência')
plt.ylabel('Razão de Financiamento por Clientes')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

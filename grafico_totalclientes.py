import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados do arquivo "contas.csv"
contas_df = pd.read_csv('./contas.csv')

# Agrupando por 'cod_agencia' e contando o número de clientes únicos
clientes_por_agencia = contas_df.groupby('cod_agencia')['cod_cliente'].nunique().reset_index()

# Renomeando colunas para melhor entendimento
clientes_por_agencia.columns = ['cod_agencia', 'numero_clientes']

# Ordenando os dados para melhor visualização
clientes_por_agencia_sorted = clientes_por_agencia.sort_values(by='numero_clientes', ascending=False)

# Plotando o gráfico de barras
plt.figure(figsize=(12, 8))
plt.bar(clientes_por_agencia_sorted['cod_agencia'].astype(str), clientes_por_agencia_sorted['numero_clientes'], color='skyblue')
plt.title('Número de Clientes por Agência')
plt.xlabel('Código da Agência')
plt.ylabel('Número de Clientes')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados (ajuste os caminhos conforme necessário)
contas_df = pd.read_csv('./contas.csv')
agencias_df = pd.read_csv('./agencias.csv')

# Mapeamento de código de agência para região (ajuste conforme seu mapeamento)
agencias_df['regiao'] = agencias_df['cod_agencia'].map({
    7: 'Sudeste', 1: 'Sudeste', 2: 'Sudeste', 3: 'Sudeste', 
    4: 'Sudeste', 8: 'Sudeste', 6: 'Sudeste', 5: 'Sul', 
    9: 'Sul', 10: 'Nordeste'
})

# Combine os DataFrames clientes_df e agencias_df para associar cada cliente à sua região
clientes_com_regiao = pd.merge(contas_df, agencias_df[['cod_agencia', 'regiao']], on='cod_agencia')

# Conte o número de clientes por região
clientes_por_regiao = clientes_com_regiao.groupby('regiao').size().reset_index(name='quantidade_clientes')

plt.figure(figsize=(10, 6))
bars = plt.bar(clientes_por_regiao['regiao'], clientes_por_regiao['quantidade_clientes'], color='skyblue')
plt.title('Quantidade de Clientes por Região', pad=20)
plt.xlabel('Região')
plt.ylabel('Quantidade de Clientes')
plt.xticks(rotation=45)

# Adicionando o número de clientes em cima de cada barra
for bar in bars:
    yval = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, yval, int(yval), va='center', ha='center', fontsize=15)

plt.tight_layout()
plt.show()


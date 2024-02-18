import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
contas_df = pd.read_csv('./contas.csv')
agencias_df = pd.read_csv('./agencias.csv')
transacoes_df = pd.read_csv('./transacoes.csv')

# Contar o número de transações por conta e criar um DataFrame
num_transacoes_por_conta = transacoes_df['num_conta'].value_counts().reset_index()
num_transacoes_por_conta.columns = ['num_conta', 'num_transacoes']

agencias_df['regiao'] = agencias_df['cod_agencia'].map({
    7: 'Sudeste', 1: 'Sudeste', 2: 'Sudeste', 3: 'Sudeste', 
    4: 'Sudeste', 8: 'Sudeste', 6: 'Sudeste', 5: 'Sul', 
    9: 'Sul', 10: 'Nordeste'
})

# Adicionar a coluna de número de transações ao DataFrame de contas
contas_com_transacoes_df = pd.merge(contas_df, num_transacoes_por_conta, on='num_conta')

contas_agencias_df = pd.merge(contas_com_transacoes_df, agencias_df[['cod_agencia', 'cidade']], on='cod_agencia')
contas_agencias_transacoes_df = pd.merge(contas_agencias_df, agencias_df[['cod_agencia', 'cidade', 'regiao']], on='cod_agencia')



# Juntando contas com agências para obter a cidade
contas_agencias_df = pd.merge(contas_com_transacoes_df, agencias_df[['cod_agencia', 'cidade']], on='cod_agencia')

# Criando o gráfico de dispersão
plt.figure(figsize=(10, 6))

for regiao in contas_agencias_transacoes_df['regiao'].unique():
    for tipo_conta in contas_agencias_transacoes_df[contas_agencias_transacoes_df['regiao'] == regiao]['tipo_conta'].unique():
        subset = contas_agencias_transacoes_df[(contas_agencias_transacoes_df['regiao'] == regiao) & (contas_agencias_transacoes_df['tipo_conta'] == tipo_conta)]
        plt.scatter(subset['num_transacoes'], subset['saldo_total'], label=f"{tipo_conta} - {regiao}")

plt.title('Clientes por Saldo e Atividade, Segmentados por Tipo de Conta e Região')
plt.xlabel('Número de Transações (Atividade)')
plt.ylabel('Saldo Total')
plt.legend(title='Tipo de Conta e Região')
plt.tight_layout()
plt.show()

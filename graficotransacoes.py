import pandas as pd
import matplotlib.pyplot as plt

# Supondo que transacoes_df e contas_df já estejam carregados
# Se necessário, substitua os caminhos abaixo pelos caminhos corretos onde os arquivos CSV estão localizados
transacoes_df = pd.read_csv('./transacoes.csv')
contas_df = pd.read_csv('./contas.csv')

# Realizar o merge do DataFrame de transações com o DataFrame de contas usando 'num_conta' como chave
transacoes_agencia_df = pd.merge(transacoes_df, contas_df[['num_conta', 'cod_agencia']], on='num_conta', how='left')

# Agrupar as transações por 'cod_agencia' e contar o número de transações para cada agência
transacoes_por_agencia = transacoes_agencia_df.groupby('cod_agencia').size().reset_index(name='num_transacoes')

# Ordenar os resultados para melhor visualização
transacoes_por_agencia_sorted = transacoes_por_agencia.sort_values(by='num_transacoes', ascending=False)

# Criar o gráfico de barras
plt.figure(figsize=(10, 6))
plt.bar(transacoes_por_agencia_sorted['cod_agencia'].astype(str), transacoes_por_agencia_sorted['num_transacoes'])
plt.xlabel('Código da Agência')
plt.ylabel('Número de Transações')
plt.title('Número de Transações por Agência')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

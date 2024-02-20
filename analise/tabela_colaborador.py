
import pandas as pd
import matplotlib.pyplot as plt

# Suponha que os DataFrames já estão carregados
propostas_credito = pd.read_csv('propostas_credito.csv')
contas = pd.read_csv('contas.csv')
colaborador_agencia = pd.read_csv('colaborador_agencia.csv')

# Filtrar apenas as propostas aprovadas
propostas_aprovadas = propostas_credito[propostas_credito['status_proposta'] == 'Aprovada']

# Associar cada proposta aprovada ao seu respectivo colaborador e agência
propostas_colaboradores = pd.merge(propostas_aprovadas, colaborador_agencia, on='cod_colaborador')

# Calcular o total do valor das propostas aprovadas por agência
total_valor_por_agencia = propostas_colaboradores.groupby('cod_agencia')['valor_proposta'].sum().reset_index(name='total_valor_proposta')

# Calcular o número total de colaboradores por agência
total_colaboradores_por_agencia = colaborador_agencia.groupby('cod_agencia').size().reset_index(name='total_colaboradores')

# Calcular o número total de clientes por agência
total_clientes_por_agencia = contas.groupby('cod_agencia')['cod_cliente'].nunique().reset_index(name='total_clientes')

# Juntar o total do valor das propostas por agência com o total de colaboradores por agência
resultado_colaboradores = pd.merge(total_valor_por_agencia, total_colaboradores_por_agencia, on='cod_agencia')

# Calcular a média do valor das propostas aprovadas por colaborador para cada agência
resultado_colaboradores['media_valor_por_colaborador'] = resultado_colaboradores['total_valor_proposta'] / resultado_colaboradores['total_colaboradores']

# Juntar o total do valor das propostas por agência com o total de clientes por agência
resultado_clientes = pd.merge(total_valor_por_agencia, total_clientes_por_agencia, on='cod_agencia')

# Calcular a média do valor das propostas aprovadas por cliente para cada agência
resultado_clientes['media_valor_por_cliente'] = resultado_clientes['total_valor_proposta'] / resultado_clientes['total_clientes']

# Juntar o total do valor das propostas por agência com o total de colaboradores e o total de clientes por agência
resultado_final = pd.merge(total_valor_por_agencia, total_colaboradores_por_agencia, on='cod_agencia')
resultado_final = pd.merge(resultado_final, total_clientes_por_agencia, on='cod_agencia')

# Calcular a média do valor das propostas aprovadas por colaborador para cada agência
resultado_final['media_valor_por_colaborador'] = resultado_final['total_valor_proposta'] / resultado_final['total_colaboradores']

# Calcular a média do valor das propostas aprovadas por cliente para cada agência
resultado_final['media_valor_por_cliente'] = resultado_final['total_valor_proposta'] / resultado_final['total_clientes']

# Renomear colunas para maior clareza
resultado_final.rename(columns={'total_colaboradores': 'total_colaboradores_agencia', 'total_clientes': 'total_clientes_agencia'}, inplace=True)

print(resultado_final)



# Ajuste o tamanho da figura conforme necessário para acomodar a tabela inteira
fig, ax = plt.subplots(figsize=(10, 6))  # Ajuste o tamanho conforme necessário
ax.axis('tight')
ax.axis('off')

# A tabela é adicionada ao gráfico
table = ax.table(cellText=resultado_final.values, colLabels=resultado_final.columns, cellLoc = 'center', loc='center')

# Ajusta a escala da tabela
table.auto_set_font_size(False)
table.set_fontsize(8)  # Ajuste o tamanho da fonte conforme necessário
table.scale(1.2, 1.2)  # Ajuste a escala da tabela conforme necessário

# Salvar a figura
plt.savefig('tabela_colaborador.png', bbox_inches='tight', dpi=300)  # Ajuste o nome do arquivo conforme necessário



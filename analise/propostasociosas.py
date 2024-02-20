import pandas as pd
import matplotlib.pyplot as plt

# Suponha que 'propostas_credito' e 'contas' são seus DataFrames carregados
propostas_credito = pd.read_csv('propostas_credito.csv')
contas = pd.read_csv('contas.csv')
clientes = pd.read_csv('clientes.csv')
colaborador_agencia = pd.read_csv('colaborador_agencia.csv')

# Agora, calcular o total de clientes por agência. Para isso, primeiro, verifique se cada conta em `contas` corresponde a um cliente único em `clientes`
contas['cliente_unico'] = contas['num_conta'].isin(clientes['cod_cliente'])
total_colaboradores_por_agencia = colaborador_agencia.groupby('cod_agencia').size().reset_index(name='total_colaboradores')

# Em seguida, calcule o total de clientes únicos por agência
total_clientes_por_agencia = contas[contas['cliente_unico']].groupby('cod_agencia').size().reset_index(name='total_clientes')

propostas_credito_agencia = pd.merge(propostas_credito, contas[['cod_cliente', 'cod_agencia']], on='cod_cliente')

total_propostas_por_agencia = propostas_credito_agencia.groupby('cod_agencia')['valor_proposta'].count()

# Calculamos o total de propostas não aceitas por agência
total_nao_aceitas_por_agencia = propostas_credito_agencia[propostas_credito_agencia['status_proposta'] != 'Aprovada'].groupby('cod_agencia')['valor_proposta'].count()

# Calculamos a proporção de propostas não aceitas por agência
proporcao_nao_aceitas_por_agencia = total_nao_aceitas_por_agencia / total_propostas_por_agencia

# Calculamos o ratio de clientes por colaborador para cada agência
clientes_por_colaborador_por_agencia = total_clientes_por_agencia.set_index('cod_agencia')['total_clientes'] / total_colaboradores_por_agencia.set_index('cod_agencia')['total_colaboradores']

# Calculamos o índice de propostas não aceitas ajustado
indice_nao_aceitas_ajustado = proporcao_nao_aceitas_por_agencia



# Agora, vamos plotar o resultado
plt.figure(figsize=(10, 6))

resultado_final = pd.DataFrame({
    'Indice Não Aceitas Ajustado': indice_nao_aceitas_ajustado,
    'Clientes por Colaborador': clientes_por_colaborador_por_agencia
}).reset_index()

# Ordenando os resultados para melhor visualização
resultado_final.sort_values('Indice Não Aceitas Ajustado', inplace=True)

plt.figure(figsize=(10, 6))
plt.bar(resultado_final['cod_agencia'].astype(str), resultado_final['Indice Não Aceitas Ajustado'], color='tomato')

# Adicionando títulos e rótulos
plt.title('Proporção de Recusadas por Propostas Totais por Agência')
plt.xlabel('Código da Agência')
plt.ylabel('Proporção de Recusadas por Propostas Totais')

# Ajustando os ticks do eixo X para mostrar todas as numerações de agência
plt.xticks(rotation=45)

plt.tight_layout()
plt.show()
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Suponha que os DataFrames já estão carregados
propostas_credito = pd.read_csv('propostas_credito.csv')
colaborador_agencia = pd.read_csv('colaborador_agencia.csv')

import pandas as pd
import matplotlib.pyplot as plt

# Suponha que os DataFrames já estão carregados
# propostas_credito = pd.read_csv('propostas_credito.csv')
# colaborador_agencia = pd.read_csv('colaborador_agencia.csv')

# Filtrar propostas com status "Aprovada"
propostas_aprovadas = propostas_credito[propostas_credito['status_proposta'] == 'Aprovada']

# Contar o número de propostas aprovadas por colaborador
propostas_por_colaborador = propostas_aprovadas.groupby('cod_colaborador').size().reset_index(name='num_propostas')

# Associar cada colaborador à sua respectiva agência
propostas_colaborador_agencia = pd.merge(propostas_por_colaborador, colaborador_agencia[['cod_colaborador', 'cod_agencia']], on='cod_colaborador')

# Para diferenciar as agências por cores, vamos atribuir uma cor para cada agência
cores_agencia = {agencia: cor for agencia, cor in zip(propostas_colaborador_agencia['cod_agencia'].unique(), plt.cm.tab20.colors)}

# Adicionar uma coluna de cores ao DataFrame baseado na agência de cada colaborador
propostas_colaborador_agencia['cor'] = propostas_colaborador_agencia['cod_agencia'].map(cores_agencia)
propostas_colaborador_agencia.sort_values(by=['cod_agencia', 'cod_colaborador'], inplace=True)

# Criar o gráfico
plt.figure(figsize=(14, 8))

# Armazenar rótulos e posições do eixo X
xticks_positions = []
xticks_labels = []

# Contador para posição no eixo X
position_counter = 0

# Iterar através do DataFrame ordenado
for _, row in propostas_colaborador_agencia.iterrows():
    plt.bar(position_counter, row['num_propostas'], color=row['cor'], label=f"Agência {row['cod_agencia']}")
    
    # Adicionar a posição e o rótulo para cada barra
    xticks_positions.append(position_counter)
    xticks_labels.append(f"{row['cod_agencia']}-{row['cod_colaborador']}")
    
    # Incrementar o contador de posição
    position_counter += 1

# Ajustar os rótulos e posições do eixo X
plt.xticks(ticks=xticks_positions, labels=xticks_labels, rotation=90)

# Ajustar a legenda para mostrar uma legenda única para cada agência
handles, labels = plt.gca().get_legend_handles_labels()
unique_labels = pd.unique(labels)
unique_handles = [handles[labels.index(label)] for label in unique_labels]
plt.legend(unique_handles, unique_labels, title='Agência', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.title('Número de Propostas de Crédito Aprovadas por Colaborador e Agência')
plt.xlabel('Agência-Colaborador')
plt.ylabel('Número de Propostas Aprovadas')
plt.tight_layout()
plt.show()


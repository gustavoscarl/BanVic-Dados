import pandas as pd
import matplotlib.pyplot as plt

# Carregar os dados
contas_df = pd.read_csv('./contas.csv')
agencias_df = pd.read_csv('./agencias.csv')
transacoes_df = pd.read_csv('./transacoes.csv')
propostas_credito_df = pd.read_csv('./propostas_credito.csv')

agencias_df['regiao'] = agencias_df['cod_agencia'].map({
    7: 'Sudeste', 1: 'Sudeste', 2: 'Sudeste', 3: 'Sudeste', 
    4: 'Sudeste', 8: 'Sudeste', 6: 'Sudeste', 5: 'Sul', 
    9: 'Sul', 10: 'Nordeste'
})

# Filtrar apenas propostas aprovadas
propostas_aprovadas_df = propostas_credito_df[propostas_credito_df['status_proposta'] == 'Aprovada']


# Juntando contas com agências para obter a cidade e região
contas_agencias_df = agencias_df[['cod_agencia', 'regiao']].merge(contas_df, on='cod_agencia')

# Combinar as propostas aprovadas com as contas para obter a agência de cada cliente
dados_combinados_df = pd.merge(propostas_aprovadas_df, contas_agencias_df, on='cod_cliente')


# Definindo uma paleta de cores para cada região
cores_regioes = {'Sudeste': 'rainbow_r', 'Sul': 'Dark2', 'Nordeste': 'grey'}

plt.figure(figsize=(12, 8))

# Iterar por região e ajustar a cor para cada agência dentro da região
for regiao, cor_base in cores_regioes.items():
    subset_regiao = dados_combinados_df[dados_combinados_df['regiao'] == regiao]
    agencias_na_regiao = subset_regiao['cod_agencia'].unique()
    num_agencias = len(agencias_na_regiao)
    
    for i, cod_agencia in enumerate(agencias_na_regiao, start=1):
        subset_agencia = subset_regiao[subset_regiao['cod_agencia'] == cod_agencia]
        # Ajuste no tom da cor baseado no índice da agência na região
        cor_agencia = plt.cm.get_cmap(cor_base)(i / num_agencias)
        plt.scatter(subset_agencia['cod_cliente'], subset_agencia['taxa_juros_mensal'], 
                    color=cor_agencia, label=f'Agência {cod_agencia} - {regiao}')

plt.title('Taxa de Juros Mensal por Cliente em Crédito Aprovado, Segmentado por Agência e Região')
plt.xlabel('Código do Cliente')
plt.ylabel('Taxa de Juros Mensal (%)')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()

import pandas as pd

# Carregar os dados dos arquivos CSV
propostas_credito = pd.read_csv('propostas_credito.csv')
contas = pd.read_csv('contas.csv')

# Filtrar propostas aprovadas
propostas_aprovadas = propostas_credito[propostas_credito['status_proposta'] == "Aprovada"]

# Cruzar dados com contas para associar cada cod_cliente com cod_agencia
propostas_com_agencia = pd.merge(propostas_aprovadas, contas[['cod_cliente', 'cod_agencia']], on='cod_cliente', how='left')

# Adicionar a coluna fisica_digital com base no cod_agencia
propostas_com_agencia['fisica_digital'] = propostas_com_agencia['cod_agencia'].apply(lambda x: 'Digital' if x == 7 else 'Física')

# Selecionar apenas as colunas desejadas
tabela_final = propostas_com_agencia[['cod_proposta', 'status_proposta', 'cod_agencia', 'valor_financiamento', 'fisica_digital']]

# Exibir a tabela final
tabela_final.to_csv('creditofxd.csv', index=False)

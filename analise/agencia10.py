import pandas as pd

# Carregar os dados (exemplo de caminho, ajuste conforme necessário)
propostas_credito = pd.read_csv('propostas_credito.csv')
colaborador_agencia = pd.read_csv('colaborador_agencia.csv')

# Filtrar apenas as propostas aprovadas
propostas_aprovadas = propostas_credito[propostas_credito['status_proposta'] == 'Aprovada']

# Associar cada proposta aprovada ao seu respectivo colaborador e agência
propostas_colaboradores_agencia = pd.merge(propostas_aprovadas, colaborador_agencia, on='cod_colaborador')

# Filtrar os colaboradores da agência 10
propostas_agencia_10 = propostas_colaboradores_agencia[propostas_colaboradores_agencia['cod_agencia'] == 10]

# Calcular o valor total das propostas aprovadas por colaborador na agência 10
valor_total_por_colaborador = propostas_agencia_10.groupby('cod_colaborador')['valor_financiamento'].sum()

# Calcular o número total de colaboradores que têm propostas aprovadas na agência 10
numero_colaboradores = valor_total_por_colaborador.count()

print(numero_colaboradores)

# Calcular o valor médio das propostas aprovadas por colaborador na agência 10
media_valor_por_colaborador = valor_total_por_colaborador.sum() / numero_colaboradores

print(f"Valor médio das propostas aprovadas por colaborador na agência 10: {media_valor_por_colaborador}")

import pandas as pd
from scipy.stats import f_oneway

# Carregar os dados
transacoes = pd.read_csv('./transacoes.csv')
contas = pd.read_csv('./contas.csv')
# Supondo que exista um arquivo para agências, caso contrário, ajuste conforme necessário
agencias = pd.read_csv('./agencias.csv')

# Desconsiderar a agência 10 de todas as operações
# Para contas
contas = contas[contas['cod_agencia'] != 10]

# Para transações, você precisa primeiro garantir que cada transação esteja ligada à sua respectiva agência
# Isso é feito associando transações com contas pelo 'num_conta'
transacoes_agencias = pd.merge(transacoes, contas[['num_conta', 'cod_agencia']], on='num_conta')

# Agora, você pode aplicar o filtro para desconsiderar transações da agência 10
transacoes_agencias = transacoes_agencias[transacoes_agencias['cod_agencia'] != 10]

# Se você também quiser aplicar o filtro diretamente nas agências
# Este passo é opcional, dependendo se você precisa trabalhar diretamente com os dados das agências
agencias = agencias[agencias['cod_agencia'] != 10]

transacoes['valor_transacao'] = transacoes['valor_transacao'].abs()

# Marcar agências como 'Física' ou 'Digital'
contas['Tipo_Agencia'] = 'Física'
contas.loc[contas['cod_agencia'] == 7, 'Tipo_Agencia'] = 'Digital'

# Filtrar transações que contêm "Crédito"
transacoes_credito = transacoes[transacoes['nome_transacao'].str.contains('Crédito', na=False)]

# Associar transações a contas para obter o tipo de agência (Física ou Digital)
transacoes_credito_com_tipo = pd.merge(transacoes_credito, contas[['num_conta', 'Tipo_Agencia']], left_on='num_conta', right_on='num_conta')

# Separar os valores de transação por tipo de agência
valores_fisica = transacoes_credito_com_tipo[transacoes_credito_com_tipo['Tipo_Agencia'] == 'Física']['valor_transacao']
valores_digital = transacoes_credito_com_tipo[transacoes_credito_com_tipo['Tipo_Agencia'] == 'Digital']['valor_transacao']


# Realizar a ANOVA
anova_result = f_oneway(valores_fisica, valores_digital)

print("F-statistic:", anova_result.statistic)
print("P-value:", anova_result.pvalue)
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats

# Carregar os dados
propostas_credito = pd.read_csv('./propostas_credito.csv')
contas = pd.read_csv('./contas.csv')

# Filtrar propostas aprovadas
propostas_aprovadas = propostas_credito[propostas_credito['status_proposta'] == "Aprovada"]

# Filtrar contas com saldo total maior que 23500
contas_filtradas_maior_23500 = contas[contas['saldo_total'] > 23500]

# Filtrar contas com saldo total menor ou igual a 23500
contas_filtradas_menor_igual_23500 = contas[contas['saldo_total'] <= 23500]

# Associar propostas aprovadas com contas filtradas por saldo maior que 23500
propostas_contas_maior_23500 = pd.merge(propostas_aprovadas, contas_filtradas_maior_23500, on='cod_cliente')

# Associar propostas aprovadas com contas filtradas por saldo menor ou igual a 23500
propostas_contas_menor_igual_23500 = pd.merge(propostas_aprovadas, contas_filtradas_menor_igual_23500, on='cod_cliente')

# Calcular o número total de clientes únicos em cada faixa de saldo
total_clientes_maior_23500 = contas_filtradas_maior_23500['cod_cliente'].nunique()
total_clientes_menor_igual_23500 = contas_filtradas_menor_igual_23500['cod_cliente'].nunique()


# Extrair os valores de financiamento para as duas faixas de saldo
valores_financiamento_maior_23500 = propostas_contas_maior_23500['valor_financiamento']
valores_financiamento_menor_igual_23500 = propostas_contas_menor_igual_23500['valor_financiamento']

print(valores_financiamento_maior_23500)
print(valores_financiamento_menor_igual_23500)

# Aplicar o teste t
t_stat, p_val = stats.ttest_ind(valores_financiamento_maior_23500, valores_financiamento_menor_igual_23500, equal_var=False)

print(f"T-statistic: {t_stat}")
print(f"P-value: {p_val}")

# Interpretar o resultado
if p_val < 0.05:
    print("Há uma diferença estatisticamente significativa entre as médias dos valores financiados nas duas faixas de saldo.")
else:
    print("Não há diferença estatisticamente significativa entre as médias dos valores financiados nas duas faixas de saldo.")
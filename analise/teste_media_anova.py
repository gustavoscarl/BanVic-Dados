from scipy.stats import f_oneway
import pandas as pd
from scipy.stats import shapiro, levene



# Supondo que 'tabela_final' seja seu DataFrame com as colunas 'cod_proposta', 'status_proposta', 'valor_financiamento', e 'fisica_digital'
tabela_final = pd.read_csv('./creditofxd.csv')
# Separar os valores de financiamento para agências físicas e digitais
valores_fisicas = tabela_final[tabela_final['fisica_digital'] == 'Física']['valor_financiamento'].tolist()
valores_digitais = tabela_final[tabela_final['fisica_digital'] == 'Digital']['valor_financiamento'].tolist()

# Realizar o teste ANOVA One-Way
f_statistic, p_value = f_oneway(valores_fisicas, valores_digitais)

# Imprimir os resultados do teste
# Teste de Shapiro-Wilk para normalidade
print(shapiro(valores_fisicas))
print(shapiro(valores_digitais))

# Teste de Levene para homogeneidade das variâncias
print(levene(valores_fisicas, valores_digitais))
print(f"F-statistic: {f_statistic}")
print(f"P-value: {p_value}")
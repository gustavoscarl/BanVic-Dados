import pandas as pd
import statsmodels.api as sm

# Suponha que 'dados' é o seu DataFrame já carregado e a coluna 'fisica_digital_cod' já esteja criada
dados = pd.read_csv('creditofxd.csv')

# Codificar a variável categórica 'fisica_digital' como numérica
# Assumindo 'Física' como 0 e 'Digital' como 1
dados['fisica_digital_cod'] = dados['fisica_digital'].map({'Física': 0, 'Digital': 1})

# Preparando os dados para regressão
X = sm.add_constant(dados['fisica_digital_cod'])  # Adiciona uma constante ao modelo
y = dados['valor_financiamento']  # Variável dependente

# Criar e ajustar o modelo de regressão linear
modelo = sm.OLS(y, X).fit()

# Mostrar o resumo do modelo
print(modelo.summary())
tabela_coeficientes = modelo.summary2().tables[1]

# Salvar o DataFrame em um arquivo CSV
tabela_coeficientes.to_csv('resumo_modelo.csv', index=True)
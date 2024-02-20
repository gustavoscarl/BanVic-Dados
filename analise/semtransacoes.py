import pandas as pd

# Carregar os dados de transações a partir do arquivo CSV correto
transacoes = pd.read_csv('./transacoes.csv')

# Gerando a lista de todos os números de conta possíveis de 1 a 999
numeros_possiveis = set(range(1, 1000))

# Extraindo os números de conta únicos presentes no DataFrame de transações
numeros_presentes = set(transacoes['num_conta'].unique())

# Identificando os números de conta ausentes
numeros_ausentes = list(numeros_possiveis - numeros_presentes)

# Mostrando os números de conta ausentes
print("Números de conta ausentes:", numeros_ausentes)

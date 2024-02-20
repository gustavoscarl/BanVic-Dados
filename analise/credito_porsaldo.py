import pandas as pd
import matplotlib.pyplot as plt

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



# Calcular a média de valor financiado para contas com saldo maior que 23500
media_financiamento_maior_23500 = propostas_contas_maior_23500['valor_financiamento'].sum() / total_clientes_maior_23500

# Calcular a média de valor financiado para contas com saldo menor ou igual a 23500
media_financiamento_menor_igual_23500 = propostas_contas_menor_igual_23500['valor_financiamento'].sum() / total_clientes_menor_igual_23500

# Criar o gráfico
plt.figure(figsize=(10, 6))
categorias = ['Saldo > 23.500', 'Saldo <= 23.500']
medias_financiamento = [media_financiamento_maior_23500, media_financiamento_menor_igual_23500]
plt.bar(categorias, medias_financiamento, color=['skyblue', 'lightgreen'])
plt.title('Média de Valor Financiado por Cliente em Faixa de Saldo')
plt.ylabel('Valor Médio de Financiamento por Cliente')
plt.show()

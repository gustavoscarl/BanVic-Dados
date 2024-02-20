import pandas as pd

# Carregar os dados
clientes = pd.read_csv('./clientes.csv')
propostas_creditos = pd.read_csv('./propostas_credito.csv')

# Calculando a idade dos clientes e categorizando em faixas etárias
clientes['ano_nascimento'] = clientes['data_nascimento'].str[:4].astype(int)
clientes['idade'] = 2024 - clientes['ano_nascimento']

bins = [18, 25, 33, 40, 50, float('inf')]
labels = ['18-25', '26-33', '34-40', '41-50', '50+']
clientes['faixa_etaria'] = pd.cut(clientes['idade'], bins=bins, labels=labels, right=False)

# Associar propostas de crédito a clientes para obter a faixa etária
propostas_clientes = pd.merge(propostas_creditos, clientes[['cod_cliente', 'faixa_etaria']], on='cod_cliente')

# Filtrando propostas com status "Aprovada"
propostas_aprovadas = propostas_clientes[propostas_clientes['status_proposta'] == 'Aprovada']

# Calculando o valor médio financiado por faixa etária
media_valor_financiado_faixa = propostas_aprovadas.groupby('faixa_etaria')['valor_financiamento'].mean().reset_index(name='media_valor_financiamento')

print(media_valor_financiado_faixa)

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(media_valor_financiado_faixa['faixa_etaria'], media_valor_financiado_faixa['media_valor_financiamento'], color='skyblue')
plt.title('Média do Valor Financiado por Faixa Etária')
plt.xlabel('Faixa Etária')
plt.ylabel('Média do Valor Financiado')
plt.xticks(rotation=45)
plt.show()

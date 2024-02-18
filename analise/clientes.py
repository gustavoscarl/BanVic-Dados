import pandas as pd

contas = pd.read_csv('./contas.csv')
clientes = pd.read_csv('./clientes.csv')


print("Códigos únicos de clientes em 'contas.csv':", contas['cod_cliente'].nunique())
print("Códigos únicos de clientes em 'clientes.csv':", clientes['cod_cliente'].nunique())

# Encontrar códigos em 'contas.csv' que não estão em 'clientes.csv'
codigos_em_contas_nao_em_clientes = set(contas['cod_cliente']) - set(clientes['cod_cliente'])
print("Códigos em contas, mas não em clientes:", codigos_em_contas_nao_em_clientes)

# Encontrar códigos em 'clientes.csv' que não estão em 'contas.csv'
codigos_em_clientes_nao_em_contas = set(clientes['cod_cliente']) - set(contas['cod_cliente'])
print("Códigos em clientes, mas não em contas:", codigos_em_clientes_nao_em_contas)

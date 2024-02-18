import pandas as pd

# Carregar os dados do arquivo "contas.csv"
contas_df = pd.read_csv('./contas.csv')

# Calculando a média do saldo líquido
media_saldo_liquido = contas_df['saldo_total'].mean()

print(f"A média do saldo total de todos os clientes do banco é: {media_saldo_liquido}\nSaldo total: {contas_df['saldo_total'].sum()}")

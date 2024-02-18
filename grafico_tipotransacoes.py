import pandas as pd
import matplotlib.pyplot as plt

# Supondo que os arquivos já foram carregados em DataFrames
transacoes_df = pd.read_csv('./transacoes.csv')
contas_df = pd.read_csv('./contas.csv')

# Filtrar apenas transações de tipos específicos e propostas aprovadas
tipos_transacoes_interesse = [
    'Saque', 'Compra Débito', 'Compra Crédito', 'DOC - Realizado',
    'TED - Realizado', 'Pagamento de boleto', 'Depósito em espécie',
    'Transferência entre CC - Débito', 'Transferência entre CC - Crédito'
]

transacoes_filtradas = transacoes_df[transacoes_df['nome_transacao'].isin(tipos_transacoes_interesse)]

# Associar transações a agências
transacoes_contas = transacoes_filtradas.merge(contas_df, on='num_conta')

# Agrupar por agência e contar o número de transações
transacoes_por_agencia = transacoes_contas.groupby('cod_agencia')['nome_transacao'].count().reset_index()
transacoes_por_agencia = transacoes_por_agencia.sort_values('nome_transacao', ascending=False)

# Continuação do seu código para plotagem
plt.figure(figsize=(10, 6))
plt.bar(transacoes_por_agencia['cod_agencia'].astype(str), transacoes_por_agencia['nome_transacao'], color='skyblue')
plt.title('Número Total de Transações por Agência - Ordenado')
plt.xlabel('Código da Agência')
plt.ylabel('Número Total de Transações')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

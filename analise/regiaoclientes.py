import pandas as pd
import matplotlib.pyplot as plt



# Carregar os dados (substitua 'caminho_para_o_arquivo' pelo caminho real dos seus arquivos)
transacoes = pd.read_csv('./transacoes.csv')
contas = pd.read_csv('./contas.csv')
propostas_credito = pd.read_csv('./propostas_credito.csv')

# Mapeamento de código de agência para região
mapa_agencias_regiao = {
    1: 'Sudeste', 2: 'Sudeste', 3: 'Sudeste', 4: 'Sudeste', 5: 'Sudeste', 6: 'Sudeste', 7: 'Sudeste',
    8: 'Sul', 9: 'Sul'
}

# Adicionar coluna de região em 'contas'
contas['regiao'] = contas['cod_agencia'].map(mapa_agencias_regiao)

# Preparar dados para cada gráfico
## Transações de crédito
transacoes_credito = transacoes[transacoes['nome_transacao'].str.contains('Crédito').abs()]
transacoes_credito_agencias = pd.merge(transacoes_credito, contas[['num_conta', 'regiao']], on='num_conta')

## Transações totais excluindo Pix
transacoes_nao_pix = transacoes[~transacoes['nome_transacao'].str.contains('Pix')]
transacoes_nao_pix_agencias = pd.merge(transacoes_nao_pix, contas[['num_conta', 'regiao']], on='num_conta')

## Financiamentos aprovados por região
propostas_aprovadas = propostas_credito[propostas_credito['status_proposta'] == 'Aprovada']
propostas_aprovadas_agencias = pd.merge(propostas_aprovadas, contas[['cod_cliente', 'regiao']], on='cod_cliente')

# Calcular o total de clientes por região
clientes_por_regiao = contas.groupby('regiao')['cod_cliente'].nunique()

# Criar os gráficos
plt.figure(figsize=(18, 6))

# Gráfico 1: Média de Transações de Crédito por Cliente por Região
plt.subplot(1, 3, 1)
trans_credito_por_regiao = transacoes_credito_agencias.groupby('regiao').size().abs() / clientes_por_regiao
trans_credito_por_regiao.plot(kind='bar', color='skyblue')
plt.title('Média de Transações de Crédito por Cliente por Região')
plt.xlabel('Região')
plt.ylabel('Média de Transações por Cliente')

# Gráfico 2: Média de Transações Totais (exceto Pix) por Cliente por Região
plt.subplot(1, 3, 2)
trans_nao_pix_por_regiao = transacoes_nao_pix_agencias.groupby('regiao').size().abs() / clientes_por_regiao
trans_nao_pix_por_regiao.plot(kind='bar', color='lightgreen')
plt.title('Média de Transações Totais (exceto Pix) por Cliente por Região')
plt.xlabel('Região')
plt.ylabel('Média de Transações por Cliente')

# Gráfico 3: Média de Financiamentos Aprovados por Cliente por Região
plt.subplot(1, 3, 3)
financ_aprov_por_regiao = propostas_aprovadas_agencias.groupby('regiao').size().abs() / clientes_por_regiao
financ_aprov_por_regiao.plot(kind='bar', color='salmon')
plt.title('Média de Financiamentos Aprovados por Cliente por Região')
plt.xlabel('Região')
plt.ylabel('Média de Financiamentos Aprovados por Cliente')

plt.tight_layout()
plt.show()

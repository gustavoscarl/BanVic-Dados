import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta

contas = pd.read_csv('./contas.csv')
agencias = pd.read_csv('./agencias.csv')
transacoes = pd.read_csv('./transacoes.csv')
financiamentos = pd.read_csv('./propostas_credito.csv')

app = dash.Dash(__name__)

total_clientes = contas['cod_cliente'].nunique()
total_transacoes = transacoes['num_conta'].nunique()
saldo_total_texto = f"R$ {contas['saldo_total'].sum():,.2f}"
total_credito_aprovado = financiamentos[financiamentos['status_proposta'] == 'Aprovada']['valor_financiamento'].sum()
total_credito_pendente = financiamentos[financiamentos['status_proposta'] != 'Aprovada']['valor_financiamento'].sum();
default_start_date = datetime.now() - timedelta(days=30)
default_end_date = datetime.now()


app.layout = html.Div([
   html.Div([
        html.Div([
            html.H3('Total de Clientes'),
            html.P(f"{total_clientes}")  # Convertendo para string
        ], style={'border': '1px solid #ddd', 'padding': '20px', 'margin': '10px', 'border-radius': '5px', 'background-color': '#f9f9f9'}),

        html.Div([
            html.H3('Total de Transações'),
            html.P(f"{total_transacoes}")  # Convertendo para string
        ], style={'border': '1px solid #ddd', 'padding': '20px', 'margin': '10px', 'border-radius': '5px', 'background-color': '#f9f9f9'}),

        html.Div([
            html.H3('Saldo Total'),
            html.P(f"{saldo_total_texto}")
        ], style={'border': '1px solid #ddd', 'padding': '20px', 'margin': '10px', 'border-radius': '5px', 'background-color': '#f9f9f9'}),
        
        html.Div([
        html.H3('Total de Crédito Financiado Aprovado'),
        html.P(f"R$ {total_credito_aprovado:,.2f}")
    ], style={'border': '1px solid #ddd', 'padding': '20px', 'margin': '10px', 'border-radius': '5px', 'background-color': '#f9f9f9'}),
        
        html.Div([
        html.H3('Total de Crédito Pendente'),
        html.P(f"R$ {total_credito_pendente:,.2f}")
    ], style={'border': '1px solid #ddd', 'padding': '20px', 'margin': '10px', 'border-radius': '5px', 'background-color': '#f9f9f9'}),
    ], style={'display': 'flex', 'justify-content': 'space-around', 'margin-top': '150px', 'text-align' : 'center', 'font-family': 'Trebuchet MS, sans-serif',}),
     html.Div([
      html.H1('Dashboard do BanVic', style={'text-align': 'center', 'margin-top': '50px'}),
      dcc.DatePickerRange(id='filtro-data',
                          start_date_placeholder_text='Data Inicial',
                          end_date_placeholder_text='Data Final',
                          initial_visible_month=transacoes['data_transacao'].min(),
                          start_date=transacoes['data_transacao'].min(),
                          end_date=transacoes['data_transacao'].max()),
      dcc.Dropdown(id='filtro-agencia', placeholder='Selecione Agência...', options=[{'label': i, 'value': i} for i in agencias['cod_agencia'].unique()], multi=True),
      dcc.Dropdown(id='filtro-cliente', placeholder='Selecione Cliente...', options=[{'label': i, 'value': i} for i in contas['cod_cliente'].unique()], multi=True),
      html.Div(id='kpi-container'),
      dcc.Graph(id='grafico-kpis')
    ]),
    # Checkbox para Selecionar/Desmarcar Todas as Agências
    html.Div([
        dcc.Checklist(
            id='selecionar-todas-checkbox',
            options=[{'label': 'Selecionar/Desmarcar Todas as Agências', 'value': 'all'}],
            value=[],
            inline=True,
             style=({
              'position': 'fixed',
              'top': '15px',
              'left': '50%',
              'transform': 'translateX(-50%)',
              'padding': '15px 13px 0px 13px',
              'zIndex': '999',
              'textAlign': 'center',
              'backgroundColor': '#f8f9fa',
              'borderRadius': '5px 5px 0px 0px',
              'boxShadow': '0 1px 2px rgba(0,0,0,0.1)'
          }),
        )
    ]),
    
    # Checklist para Seleção de Múltiplas Agências
    html.Div([
        dcc.Checklist(
            id='agencia-checklist',
            options=[{'label': i, 'value': i} for i in contas['cod_agencia'].unique()],
            value=list(contas['cod_agencia'].unique()),
            inline=True,
            style=({
              'position': 'fixed',
              'top': '50px',
              'left': '50%', 
              'transform': 'translateX(-50%)',
              'paddingTop': '20px',
              'zIndex': '999',
              'textAlign': 'center',
              'backgroundColor': '#f8f9fa',
              'borderRadius': '0px 0px 5px 5px',  
              'padding': '10px',  
              'boxShadow': '0 1px 2px rgba(0,0,0,0.1)'  
          }),
        )
    ]),
    # Gráficos como definido anteriormente
    dcc.Graph(id='grafico-financiamentos-aprovados'),
    dcc.Graph(id='grafico-media-saldo'),
    dcc.Graph(id='grafico-transacoes-tipo'),
    dcc.Graph(id='grafico-ratio-clientes'),
])

@app.callback(
    Output('agencia-checklist', 'value'),
    [Input('selecionar-todas-checkbox', 'value')],
    [State('agencia-checklist', 'options')]
)
def selecionar_desmarcar_todas(selected_all, options):
    if 'all' in selected_all:
        return [option['value'] for option in options]
    return []

# Callbacks para atualizar cada gráfico com base na seleção da agência
@app.callback(
    [Output('grafico-financiamentos-aprovados', 'figure'),
     Output('grafico-media-saldo', 'figure'),
     Output('grafico-transacoes-tipo', 'figure'),
     Output('grafico-ratio-clientes', 'figure')],
    [Input('agencia-checklist', 'value')]
)



def update_graphs(selected_agencias):

    # Gráfico 1 - Taxa de Financiamentos Aprovados/Cliente
    financiamentos_aprovados = financiamentos[financiamentos['status_proposta'] == 'Aprovada']
    clientes_por_agencia = contas.groupby('cod_agencia')['cod_cliente'].nunique()
    
    grafico_financiamentos = go.Figure()
    
    for agencia in selected_agencias:
        # Filtrar financiamentos aprovados por agência
        financiamentos_agencia = financiamentos_aprovados[financiamentos_aprovados['cod_cliente'].isin(contas[contas['cod_agencia'] == agencia]['cod_cliente'])]
        
        # Calcular o total de financiamentos aprovados
        total_financiamentos_aprovados = len(financiamentos_agencia)
        
        # Obter o número total de clientes para a agência
        total_clientes = clientes_por_agencia.get(agencia, 0)
        
        # Calcular a razão, evitando divisão por zero
        razao = total_financiamentos_aprovados / total_clientes if total_clientes else 0
        
        # Adicionar barra ao gráfico para a agência atual
        grafico_financiamentos.add_trace(go.Bar(x=[f"Agência {agencia}"], y=[razao], name=f"Agência {agencia}"))
    
    grafico_financiamentos.update_layout(
        title_text='Taxa de Financiamentos Aprovados/Cliente em Agência Selecionada(s)',
        xaxis_title='Agência',
        yaxis_title='Total de Financiamentos Aprovados/Clientes',
        legend_title='Agência'
    )
    if not selected_agencias:
    # Se não houver agências selecionadas, retorne um gráfico vazio ou com uma mensagem
      grafico_financiamentos.add_trace(go.Bar(x=[], y=[], name="Nenhuma agência selecionada"))

      
    # Gráfico 2 - Media Saldo
    contas['cod_agencia'] = contas['cod_agencia'].astype(int)
    average_balance = contas.groupby('cod_agencia')['saldo_total'].mean().reset_index()
    average_balance_sorted = average_balance.sort_values(by='cod_agencia')
    average_balance_filtered = average_balance_sorted[average_balance_sorted['cod_agencia'].between(1, 10)]

    # Now create your pie chart with the sorted and filtered data
    grafico_media_saldo = go.Figure(data=[go.Pie(
        labels=average_balance_filtered['cod_agencia'].astype(str),
        values=average_balance_filtered['saldo_total'],
        hoverinfo='label+percent',
        textinfo='value'
    )])

    grafico_media_saldo.update_layout(
        title='Média do Saldo Total por Cliente por Agência',
        legend_title='Agência'
    )


    #Gráfico 3 - Transações de Crédito por Agência
    transacoes_credito = transacoes[transacoes['nome_transacao'].str.contains('Crédito')].copy()
    transacoes_credito['valor_transacao'] = transacoes_credito['valor_transacao'].abs()

    # Agrupar as transações por 'cod_cliente' e somar os valores de 'valor_transacao'
    transacoes_por_cliente = transacoes_credito.groupby('num_conta')['valor_transacao'].sum().reset_index()

    # Unir com 'contas' para obter o 'cod_agencia' correspondente a cada cliente
    transacoes_com_agencia = pd.merge(transacoes_por_cliente, contas[['num_conta', 'cod_agencia']], on='num_conta')

    # Agrupar as transações por 'cod_agencia' e somar os valores para obter o total por agência
    transacoes_por_agencia = transacoes_com_agencia.groupby('cod_agencia')['valor_transacao'].sum().reset_index()

    # Selecionar agências  # Exemplo de agências selecionadas

    # Filtrar as transações pela seleção de agências
    transacoes_selecionadas = transacoes_por_agencia[transacoes_por_agencia['cod_agencia'].isin(selected_agencias)]

    # Criar o gráfico de barras
    grafico_transacoes_credito_por_agencia = go.Figure()

    for agencia in selected_agencias:
        valor_transacao = transacoes_selecionadas[transacoes_selecionadas['cod_agencia'] == agencia]['valor_transacao'].iloc[0]
        grafico_transacoes_credito_por_agencia.add_trace(go.Bar(
            x=[f"Agência {agencia}"],
            y=[valor_transacao],
            name=f"Agência {agencia}"
        ))

    grafico_transacoes_credito_por_agencia.update_layout(
        title_text='Total de Transações de Crédito por Agência',
        xaxis_title='Agência',
        yaxis_title='Total de Transações de Crédito',
        legend_title='Agência'
    )


    # Gráfico 4 - Calculando a razão de clientes por financiamento aprovado por agência
    financiamentos_aprovados = financiamentos[financiamentos['status_proposta'] == 'Aprovada']

    # Realize a fusão com contas_df para obter os códigos das agências.
    merged = financiamentos_aprovados.merge(contas[['cod_cliente', 'cod_agencia']], on='cod_cliente')

    # Agora, calcule o valor total de financiamentos aprovados por agência.
    valor_por_agencia = merged.groupby('cod_agencia')['valor_financiamento'].sum()

# Calcule o número total de clientes por agência.
    clientes_por_agencia = contas.groupby('cod_agencia')['cod_cliente'].nunique()

# Crie o gráfico.
    grafico_ratio_clientes = go.Figure()

    for agencia in selected_agencias:
      total_financiamentos = valor_por_agencia.get(agencia, 0)
      total_clientes = clientes_por_agencia.get(agencia, 0)
    
  # Calcular a razão, evitando divisão por zero
      razao = total_financiamentos / total_clientes if total_clientes > 0 else 0
    
    # Adicione a barra ao gráfico para a agência atual
      grafico_ratio_clientes.add_trace(go.Bar(
        x=[f"Agência {agencia}"],
        y=[razao],
        name=f"Agência {agencia}",
        text=[f"{razao:.2f}"],
        textposition='auto'
    ))

    grafico_ratio_clientes.update_layout(
  title_text='Razão do Total de Financiamentos Aprovados/Clientes por Agência',
  xaxis_title='Agência',
  yaxis_title='Total em R$ de Financiamento Aprovado',
  legend_title='Agência'
)

    # Substitua o retorno adequado para incluir grafico_ratio_financiamento
    
    return grafico_financiamentos, grafico_media_saldo, grafico_transacoes_credito_por_agencia, grafico_ratio_clientes

if __name__ == '__main__':
  app.run_server(debug=True)
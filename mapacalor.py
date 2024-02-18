import pandas as pd
import plotly.express as px

# Substitua '/caminho/para/' pelos caminhos reais dos seus arquivos
caminho_contas = './contas.csv'
caminho_agencias = './agencias.csv'

# Carregar os DataFrames
contas_df = pd.read_csv(caminho_contas)
agencias_df = pd.read_csv(caminho_agencias)

# Agregar o saldo total por agência em 'contas_df'
saldo_total_por_agencia = contas_df.groupby('cod_agencia')['saldo_total'].sum().reset_index()

# Realizar o merge dos dados agregados com as informações das agências
dados_completos = pd.merge(saldo_total_por_agencia, agencias_df, on='cod_agencia')

fig = px.scatter_geo(dados_completos,
                     lat='lat',
                     lon='long',
                     size='saldo_total',  # O tamanho do marcador reflete o saldo total
                     hover_name='nome',  # Mostra o nome da agência ao passar o mouse
                     projection="mercator",  # Projeção do mapa
                     title="Saldo Total por Agência em Todo o Brasil",
                     size_max=80)

# Ajustar os limites geográficos para focar no Brasil
fig.update_geos(
    lataxis_range=[-33, 5],  # Limites de latitude para cobrir o Brasil
    lonaxis_range=[-74, -34],  # Limites de longitude para cobrir o Brasil
    visible=False  # Oculta os detalhes geográficos padrão para um visual mais limpo
)

# Habilitar o mapa de base (opcional)
fig.update_layout(geo=dict(bgcolor= 'rgba(0,0,0,0)',
                           lakecolor='rgba(127,205,255,0.5)',
                           landcolor='#fff',
                           showland=True,
                           countrycolor='black',
                           showcountries=True))

fig.show()

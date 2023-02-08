import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html


# Código do gráfico transformado em função:

def gera_media_continente(variavel):
  def adicionar_valor(pontuacao, continentes, comparacao):
    lista = []
    for i in range(len(pontuacao)):
      if continentes[i] == comparacao:
        lista.append(pontuacao[i])
    return lista


# Função que calcula média dos continentes com base na pontuação de seus respectivos países
  def media(lista):
    total = 0
    for i in range(len(lista)):
      a = lista[i]
      total = a + total
    media = total/len(lista)
    return("%.3f"%media)

  # Importando arquivo e atribuindo às variáveis as colunas necessárias para realizar o  gráfico
  df = pd.read_csv("C:\ProjetosVSCode\Python\Test\data\BrunoData.csv",sep=';')
  pontuacao =df[variavel]
  paises =df['Country']
  continentes = df['Continente']

  # Separando em listas a pontuação de felicidade de cada país com base em seu continente 
  lista_NAm = adicionar_valor(pontuacao, continentes, 'North - America')
  lista_SAm = adicionar_valor(pontuacao, continentes, 'South - America')
  lista_Eu = adicionar_valor(pontuacao, continentes, 'Europe')
  lista_Asia = adicionar_valor(pontuacao, continentes,'Asia')
  lista_Afri = adicionar_valor(pontuacao, continentes,'Africa')
  lista_Oce = adicionar_valor(pontuacao, continentes,'Oceania')

  # Calculando média de felicidade de cada continente:
  media_Eu = media(lista_Eu)
  media_NAm = media(lista_NAm)
  media_SAm = media(lista_SAm)
  media_Asia = media(lista_Asia)
  media_Afri = media(lista_Afri)
  media_Oce = media(lista_Oce)

  # Atribuindo a cada país a média do continente ao qual ele pertence e ordenando esses valores na lista haver_paises
  haver_paises = []

  for i in range(len(continentes)):
    if continentes[i] == 'Europe':
      haver_paises.append(media_Eu)
    elif continentes[i] == 'North - America':
      haver_paises.append(media_NAm)
    elif continentes[i] == 'South - America':
      haver_paises.append(media_SAm)
    elif continentes[i] == 'Asia':
      haver_paises.append(media_Asia)
    elif continentes[i] == 'Africa':
      haver_paises.append(media_Afri)
    elif continentes[i] == 'Oceania':
      haver_paises.append(media_Oce)

  # Gerando o gráfico que demonstra a média de pontuação de felicidade de cada continente 
  fig = px.choropleth(locationmode = 'country names',locations = paises, color = haver_paises, hover_name = continentes,
                     projection = 'natural earth',)
  return fig


# Código que cria o dash:

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# A função vai mostrar a média por continente de cada variável
fig = gera_media_continente('Score')

opcoes = ['Score','GDP per capita', 'Social support', 'Healthy life expectancy', 'Freedom to make life choices', 'Generosity', 'Perceptions of corruption']

app.layout = html.Div(children=[
    html.H1(children='Média dos Continentes'),

    html.H3(children = 'Este demonstra a média de cada continente com base na escolha da variáv'),

    dcc.Dropdown(opcoes, value = 'Score',id='op_variaveis'),

    dcc.Graph(
        id='grafico_continente',
        figure=fig
    )
])

@app.callback(
    dash.dependencies.Output('grafico_continente','figure'),
    dash.dependencies.Input('op_variaveis', 'value')
)

def altera_grafico(value):
  fig = gera_media_continente(value)
  return fig

if __name__ == '__main__':
    app.run_server(mode = "external")
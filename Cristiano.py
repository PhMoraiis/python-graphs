
#PARTE DE IMPORTAÇÃO
#
#
from dash import Dash,html,dcc
import plotly.express as px
import pandas as pd
from dash import Input,Output
#
#
#RECEPÇÃO DOS DADOS NA VARIAVEL TAB

tab = pd.read_csv("C:\ProjetosVSCode\Python\Test\data\CristianoData.csv")
#
#
# ALOCAÇÃO DE DADOS NAS VARIÁVEIS A SEREM UTILIZADAS POSTERIORMENTE PARA O CÁLCULO DO PERCENTUAL

rank_pais = tab['Country or region']
renda = tab['GDP per capita']
pontos = tab['Score']
suporte_social = tab['Social support']
saude = tab['Healthy life expectancy']
liberdade = tab['Freedom to make life choices']
generosidade = tab['Generosity']
corrupcao = tab['Perceptions of corruption']

variaveis = [renda,suporte_social,saude,liberdade,generosidade,corrupcao]
#
#
#
#
# CRIAÇÃO DE FUNÇÃO PARA REALIZAÇÃO DE CÁLCULO UTILIZANDO AS VARIÁVEIS E PLOTAGEM DO GRÁFICO DE ACORDO COM A VARIÁVEL ESCOLHIDA

def calculo(variaveis):
  recebe = ''
  if variaveis == 'Renda':
    recebe = renda
  if variaveis == 'Suporte social':
    recebe = suporte_social
  if variaveis == 'Saúde':
    recebe = saude
  if variaveis == 'Liberdade':
    recebe = liberdade
  if variaveis == 'Generosidade':
    recebe = generosidade
  if variaveis == 'Corrupção':
    recebe = corrupcao
  
  razao = []
  x = ((recebe)/(pontos))*100
  razao.append(x)
  
  fig = px.line(x = rank_pais, y = razao, title = f'Variável utilizada:{variaveis}')

  fig.update_yaxes(title = 'Percentual',showgrid= False)

  fig.update_xaxes(title = 'País/Região',showgrid= False)

  return fig

#
#
#
# PRODUÇÃO DO DASH 

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)

fig = calculo('Renda')


colors = {
    'background': '#111111',
    'text': '#EE82EE'}


app.layout = html.Div(children=[
    html.H1(id='titulo', children='Representação percentual em relação a pontuação geral', style={
            'textAlign': 'center',
            'color' : '#000000'}),
    
    
     dcc.RadioItems(
        id = 'Escolha',
        options = ['Renda','Suporte social','Saúde','Liberdade','Generosidade','Corrupção'],
        value = 'Renda',
        style = { 'color' : colors['text']}),

    dcc.Graph(id='grafico', figure=fig)

    
                                    
  ])

@app.callback(
    Output('grafico','figure'),
    Input('Escolha','value')

)

def muda_grafico(value):
  fig = calculo(value)
  return fig


  
if __name__ == '__main__':
  app.run_server(debug = True)
  
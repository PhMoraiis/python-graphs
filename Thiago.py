import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html
#import plotly.express as px
#import plotly.graph_objects as go
#from dash.dependencies import Input,Output

dados = pd.read_csv('C:\ProjetosVSCode\Python\Test\data\ThiagoData.csv',sep=';')
#Define a lista

#Cria nova lista vazia para implementação dos novos valores
score = dados['Score']
support = dados['Social support']
continente = dados['Continente']

def criar_listas(score,support,continente,comparacao):
  lista = []
  
  for i in range(len(continente)):
    if continente[i] == comparacao :
      lista.append([score[i],support[i]])
      
  return lista

#Separando em listas a pontuação de felicidade de cada país com base em seu continente 
lista_NAm = criar_listas(score, support,continente, 'North - America')
lista_SAm = criar_listas(score, support,continente, 'South - America')
lista_Eu = criar_listas(score, support,continente, 'Europe')
lista_Asia = criar_listas(score, support,continente,'Asia')
lista_Afri = criar_listas(score, support,continente,'Africa')
lista_Oce = criar_listas(score, support,continente,'Oceania')

novo_dataframe = pd.DataFrame(lista_Eu, columns= ["Score","Suporte Social"])

fig = px.scatter(data_frame = novo_dataframe, x ="Score", y = "Suporte Social")

app.layout = html.Div([
  html.H1('Gráfico de Dispersão - Score x Suporte Social'),
  html.H2('Escolha o continente'),
  dcc.Dropdown(
      id='dropdown',
      options=[
          {'label': 'Europa','value': 'Europa'},
          {'label': 'North - America','value': 'North - America'},
          {'label': 'South - America','value': 'South - America'},
          {'label': 'Asia','value': 'Asia'},
          {'label': 'Africa','value': 'Africa'},
          {'label': 'Oceania','value': 'Oceania'},
      ],
      value='Europa'
  ),
  dcc.Graph( 
      id='dispersao-graph',
      figure=fig,
  ),
 ])

@app.callback(
    dash.dependencies.Output(component_id='dispersao-graph',component_property='figure'),
    dash.dependencies.Input(component_id='continente', component_property='value')
)

def trocar_variaveis(value):
  if value == 'Europa':
    novo_dataframe = pd.DataFrame(lista_Eu, columns= ["Score","Suporte Social"])
    return px.scatter(data_frame = novo_dataframe, x ="Score", y = "Suporte Social")
  elif value == 'North - America':
    novo_dataframe = pd.DataFrame(lista_NAm, columns= ["Score","Suporte Social"])
    return px.scatter(data_frame = novo_dataframe, x ="Score", y = "Suporte Social")
  elif value == 'South - America':
    novo_dataframe = pd.DataFrame(lista_SAm, columns= ["Score","Suporte Social"])
    return px.scatter(data_frame = novo_dataframe, x ="Score", y = "Suporte Social")
  elif value == 'Asia':
    novo_dataframe = pd.DataFrame(lista_Asia, columns= ["Score","Suporte Social"])
    return px.scatter(data_frame = novo_dataframe, x ="Score", y = "Suporte Social")
  elif value == 'Africa':
    novo_dataframe = pd.DataFrame(lista_Afri, columns= ["Score","Suporte Social"])
    return px.scatter(data_frame = novo_dataframe, x ="Score", y = "Suporte Social")
  elif value == 'Oceania':
    novo_dataframe = pd.DataFrame(lista_Oce, columns= ["Score","Suporte Social"])
    return px.scatter(data_frame = novo_dataframe, x ="Score", y = "Suporte Social")      

if __name__ == '__main__' :
  app.run_server(debug=True)
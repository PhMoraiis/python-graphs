import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html


# Lê o arquivo csv
position_var=pd.read_csv("C:\ProjetosVSCode\Python\Test\data\AllSheets.csv", sep=',')
percentual_graph = pd.read_csv("C:\ProjetosVSCode\Python\Test\data\CristianoData.csv", sep=',')
continental_graph = pd.read_csv("C:\ProjetosVSCode\Python\Test\data\BrunoData.csv",sep=';')
dispersao_graph = pd.read_csv('C:\ProjetosVSCode\Python\Test\data\ThiagoData.csv',sep=';')

# Inicializa o dashboard
app = dash.Dash(__name__, external_stylesheets=['https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600;700;800;900&display=swap'])


# GRAFICO CAMILA E PHILIPE

# Filtragem dos dados para usar no dropdown da VARIAÇÃO DA POSIÇÃO
position_var = position_var[position_var["Country"].notnull()]
## Verifica se o país não é nulo

optionsCountry = [{"label": pais, "value": pais} for pais in position_var['Country'].unique()]
## Verifica e impede a duplicação de países no dropdown

# Callback para atualizar o gráfico de acordo com o país selecionado (VARIAÇÃO DA POSIÇÃO)
@app.callback(
    dash.dependencies.Output('grafico-variacao', 'figure'),
    dash.dependencies.Input('pais', 'value')
)

# Função para atualizar o gráfico (VARIAÇÃO DA POSIÇÃO)
def update_figure(pais):
  ## Pega os dados para usar nos eixos do gráfico
  anos = ['2015', '2016', '2017', '2018', '2019']
  rankings = []
  for index, row in position_var.iterrows():
      if row['Country'] == pais:
          rankings.append(row['Happiness Rank'])

  ## Montagem do gráfico
  fig = px.line(x= anos, y= rankings, title=f'Variação da Posição do(a) {pais} no Ranking da Felicidade', template='plotly_white')
  fig.update_traces(hovertemplate='<b>Ano: %{x}</b><br><b>Posição: %{y}</b>',hoverlabel=dict(bgcolor="white", font_size=16, font_family="Poppins"))
  fig.update_traces(name='Variação da Posição', mode='lines+markers', line=dict(color='#3EECAC', width=3), marker=dict(color='#EE74E1', size=10))
  fig.update_yaxes(title='Posições no Ranking')
  fig.update_xaxes(title='Anos')
  fig.update_layout(font_family='Poppins', font_color='#666', title_font_family='Poppins', title_font_color='#666', title_font_size=20, title_x=0.5, title_y=0.95, title_xanchor='center', title_yanchor='top',
  paper_bgcolor='#F5F5F5', plot_bgcolor='#c8c8c8')

  return fig


# GRÁFICO CRISTIANO

# Alocação de dados nas variáveis a serem utilizadas posteriormente para o cálculo do percentual
rank_pais = percentual_graph['Country or region']
renda = percentual_graph['GDP per capita']
pontos = percentual_graph['Score']
suporte_social = percentual_graph['Social support']
saude = percentual_graph['Healthy life expectancy']
liberdade = percentual_graph['Freedom to make life choices']
generosidade = percentual_graph['Generosity']
corrupcao = percentual_graph['Perceptions of corruption']

variaveis = [renda,suporte_social,saude,liberdade,generosidade,corrupcao]

# Criação de função para realização de cálculo utilizando as variáveis e plotagem do gráfico de acordo com a variável escolhida
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
  
  fig = px.line(x = rank_pais, y = razao, title = f'Variável utilizada: {variaveis}', template='plotly_white')
  fig.update_traces(hovertemplate='<b>Pais: %{x}</b><br><b>Razão: %{y}</b>',hoverlabel=dict(bgcolor="white", font_size=16, font_family="Poppins"))
  fig.update_traces(name=f'{variaveis}', mode='lines+markers', line=dict(color='#3EECAC', width=3), marker=dict(color='#EE74E1', size=10))
  fig.update_yaxes(title = 'Percentual',showgrid= False)
  fig.update_xaxes(title = 'País/Região',showgrid= True)
  fig.update_layout(font_family='Poppins', font_color='#666', title_font_family='Poppins', title_font_color='#666', title_font_size=20, title_x=0.5, title_y=0.95, title_xanchor='center', title_yanchor='top', paper_bgcolor='#F5F5F5', plot_bgcolor='#c8c8c8')

  return fig

@app.callback(
    dash.dependencies.Output('grafico-percentual','figure'),
    dash.dependencies.Input('Escolha','value')
)

def muda_grafico(value):
  fig = calculo(value)
  return fig

# Geração do gráfico

# GRÁFICO BRUNO

def gera_media_continente(variavel, visualizacao):
  #Função que separa a pontuação dos países em listas com base no continente ao qual fazem parte.
  def adicionar_valor(pontuacao, continentes, comparacao):
    lista = []
    for i in range(len(pontuacao)):
      if continentes[i] == comparacao:
        lista.append(pontuacao[i])
    return lista


#Função que calcula média dos continentes com base na pontuação de seus respectivos países
  def media(lista):
    total = 0
    for i in range(len(lista)):
      a = lista[i]
      total = a + total
    media = total/len(lista)
    return("%.3f"%media)

  #Importando arquivo e atribuindo às variáveis as colunas necessárias para realizar o  gráfico
  pontuacao =continental_graph[variavel]
  paises =continental_graph['Country']
  continentes = continental_graph['Continente']

  #Separando em listas a pontuação de felicidade de cada país com base em seu continente 
  lista_NAm = adicionar_valor(pontuacao, continentes, 'North - America')
  lista_SAm = adicionar_valor(pontuacao, continentes, 'South - America')
  lista_Eu = adicionar_valor(pontuacao, continentes, 'Europe')
  lista_Asia = adicionar_valor(pontuacao, continentes,'Asia')
  lista_Afri = adicionar_valor(pontuacao, continentes,'Africa')
  lista_Oce = adicionar_valor(pontuacao, continentes,'Oceania')

  #Calculando média de felicidade de cada continente:
  media_Eu = media(lista_Eu)
  media_NAm = media(lista_NAm)
  media_SAm = media(lista_SAm)
  media_Asia = media(lista_Asia)
  media_Afri = media(lista_Afri)
  media_Oce = media(lista_Oce)
  
  media_continentes = [media_Eu, media_NAm, media_SAm, media_Asia, media_Afri, media_Oce]

  #Atribuindo a cada país a média do continente ao qual ele pertence e ordenando esses valores na lista haver_paises
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

  #Gerando o gráfico que demonstra a média de pontuação de cada continente. 
  fig = px.choropleth(
    locationmode = 'country names',
    locations = paises, 
    color = haver_paises, 
    hover_name = continentes,
    projection = 'natural earth',
  )
  #Gerando o gráfico em formato de pizza.
  fig2 = px.pie(
    names = ['Europe', 'North - America', 'South - America', 'Asia', 'Africa', 'Oceania'], 
    values = media_continentes
  )

  #Retorno do gráfico com base na opção de visualização escolhida pelo usuário
  if visualizacao == 'Geomapa':
    return fig
  else:
    return fig2

opcoes = ['Score','GDP per capita', 'Social support', 'Healthy life expectancy', 'Freedom to make life choices', 'Generosity', 'Perceptions of corruption']

@app.callback(
    dash.dependencies.Output('grafico_continente','figure'),
    dash.dependencies.Input('op_variaveis', 'value'),
    dash.dependencies.Input('visualizacao', 'value')
)

def altera_grafico(variavel, visualizacao):
  fig = gera_media_continente(variavel,visualizacao)
  return fig


## GRAFICO THIAGO
#Cria nova lista vazia para implementação dos novos valores
score = dispersao_graph['Score']
support = dispersao_graph['Social support']
continente = dispersao_graph['Continente']

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

@app.callback(
    dash.dependencies.Output('dispersao-graph','figure'),
    dash.dependencies.Input('continente', 'value')
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

# Layout do dashboard com o dropdown para selecionar o país (VARIAÇÃO DA POSIÇÃO)
app.layout = html.Section([
    html.Div(
    style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',},
    children=[html.H1('Dashboard da Felicidade', style={'fontFamily': 'Poppins', 'textAlign': 'center', 'fontSize': '2.5rem', 'background': '-webkit-linear-gradient(19deg, #EE74E1, #3EECAC 80%)','-webkit-background-clip': 'text','-webkit-text-fill-color': 'transparent', 'margin': '0'}),
    html.H1('😄', 
    style={'fontFamily': 'Poppins', 'textAlign': 'center', 'fontSize': '2.5rem', 'marginLeft': '0.5rem','margin': '0'})]),

    html.H3('Selecione um país para ver a variação da posição no ranking da felicidade:', 
    style={'fontFamily': 'Poppins', 'textAlign': 'center', 'fontSize': '1.5rem', 'background': '-webkit-linear-gradient(45deg, #EE74E1, #3EECAC 80%)','-webkit-background-clip': 'text','-webkit-text-fill-color': 'transparent'}),
    dcc.Dropdown(
    id='pais',
    options=optionsCountry,
    style={'fontFamily': 'Poppins', 'width': '50%', 'borderRadius': '5px', 'color': '#666', 'margin': '0 auto', 'display': 'block'},
    clearable=False,
    searchable=False,
    placeholder='Selecione um país'
    ),
    html.Br(),
    dcc.Graph(
    id='grafico-variacao', 
    style={'borderRadius': '20px', 'width': '100%', 'margin': '0 auto', 'display': 'block'}),


    html.Section([
    html.H3('Representação percentual em relação a pontuação geral',
      id='titulo', 
      style={'fontFamily': 'Poppins', 'textAlign': 'center', 'fontSize': '1.5rem', 'background': '-webkit-linear-gradient(45deg, #EE74E1, #3EECAC 80%)','-webkit-background-clip': 'text','-webkit-text-fill-color': 'transparent'} 
    ),
    dcc.Dropdown(
      id = 'Escolha',
      options = ['Renda','Suporte social','Saúde','Liberdade','Generosidade','Corrupção'],
      value = 'Renda',
      style={'fontFamily': 'Poppins', 'width': '50%', 'borderRadius': '5px', 'color': '#666', 'margin': '0 auto', 'display': 'block'}
    ),
    html.Br(),
    dcc.Graph(
      id='grafico-percentual', 
      style={'borderRadius': '20px', 'width': '100%', 'margin': '0 auto', 'display': 'block'})                             
  ], style={'marginTop': '2rem'}),

    html.Section([
    html.H3('Média dos Continentes',
    style={'fontFamily': 'Poppins', 'textAlign': 'center', 'fontSize': '1.5rem', 'background': '-webkit-linear-gradient(45deg, #EE74E1, #3EECAC 80%)','-webkit-background-clip': 'text','-webkit-text-fill-color': 'transparent'}
    ),
    html.H4(
    'Este demonstra a média de cada continente com base na escolha da variável',
    style={'fontFamily': 'Poppins', 'textAlign': 'center', 'background': '-webkit-linear-gradient(45deg, #EE74E1, #3EECAC 80%)','-webkit-background-clip': 'text','-webkit-text-fill-color': 'transparent'}
    ),
    dcc.Dropdown(
    options=opcoes,
    id='op_variaveis',
    value = 'Score',
    style={'fontFamily': 'Poppins', 'width': '50%', 'borderRadius': '5px', 'color': '#666', 'margin': '0 auto', 'display': 'block'}
    ),
    html.H4('Escolha a opção de visualização do gráfico',
    style={'fontFamily': 'Poppins', 'textAlign': 'center', 'fontSize': '1.5rem', 'background': '-webkit-linear-gradient(45deg, #EE74E1, #3EECAC 80%)','-webkit-background-clip': 'text','-webkit-text-fill-color': 'transparent'}),
    dcc.RadioItems(
        id = 'visualizacao',
        options = ['Geomapa', 'Pizza'],
        value = 'Geomapa',
        inline = True,
        style={'fontFamily': 'Poppins', 'width': '100%', 'borderRadius': '5px', 'color': '#666', 'margin': '0 0 30px', 'display': 'inline-block', 'textAlign': 'center', 'fontSize': '1.2rem'}
    ),
    html.Br(),
    dcc.Graph(
    id='grafico_continente',
    style={'borderRadius': '20px', 'width': '100%', 'margin': '0 auto', 'display': 'block'}
    )
  ], style={'marginTop': '2rem'}),

    html.Section([
    html.H3(
    'Gráfico de Dispersão - Score x Suporte Social',
    style={'fontFamily': 'Poppins', 'textAlign': 'center', 'fontSize': '1.5rem', 'background': '-webkit-linear-gradient(45deg, #EE74E1, #3EECAC 80%)','-webkit-background-clip': 'text','-webkit-text-fill-color': 'transparent'}),
    html.H4(
    'Escolha o continente',
    style={'fontFamily': 'Poppins', 'textAlign': 'center', 'background': '-webkit-linear-gradient(45deg, #EE74E1, #3EECAC 80%)','-webkit-background-clip': 'text','-webkit-text-fill-color': 'transparent'}),
    dcc.Dropdown(
        id='continente',
        options=[
            {'label': 'Europa','value': 'Europa'},
            {'label': 'North - America','value': 'North - America'},
            {'label': 'South - America','value': 'South - America'},
            {'label': 'Asia','value': 'Asia'},
            {'label': 'Africa','value': 'Africa'},
            {'label': 'Oceania','value': 'Oceania'},
        ],
        value='Europa',
        style={'fontFamily': 'Poppins', 'width': '50%', 'borderRadius': '5px', 'color': '#666', 'margin': '0 auto', 'display': 'block'}
    ),
    dcc.Graph( 
        id='dispersao-graph',
        figure=fig,
    ),
  ], style={'background': '#F5F5F5'})
], style={'background': '#F5F5F5'})

# Executa o dashboard
if __name__ == '__main__':
    app.run_server(debug=True)
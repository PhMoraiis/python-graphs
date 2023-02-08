import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html

# Lê os arquivos csv
positionVar=pd.read_csv("C:\ProjetosVSCode\Python\Test\data\AllSheets.csv", sep=',')
crisDash = pd.read_csv("C:\ProjetosVSCode\Python\Test\data\CristianoData.csv", sep=',')

# Inicializa o dashboard
app = dash.Dash(__name__, external_stylesheets=['https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600;700;800;900&display=swap'])



# Filtragem dos dados para usar no dropdown da VARIAÇÃO DA POSIÇÃO
positionVar_filtered = []
for index, row in enumerate(positionVar):
    if row["Country"] != None:
        positionVar_filtered.append(row)
## Verifica os países que estão no dataset e remove os que são nulos

paises = set()
for index, row in positionVar_filtered.iterrows():
    paises.add(row['Country'])

optionsCountry = [{"label": pais, "value": pais} for pais in paises]
## Verifica e impede a duplicação de países no dropdown

# Layout do dashboard com o dropdown para selecionar o país (VARIAÇÃO DA POSIÇÃO)
app.layout = html.Div([
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
    dcc.Graph(id='grafico-felicidade', style={'borderRadius': '20px', 'width': '100%', 'margin': '0 auto', 'display': 'block'})
], style={'background': '#F5F5F5'})

# Callback para atualizar o gráfico de acordo com o país selecionado (VARIAÇÃO DA POSIÇÃO)
@app.callback(
    dash.dependencies.Output('grafico-felicidade', 'figure'),
    dash.dependencies.Input('pais', 'value')
)

# Função para atualizar o gráfico (VARIAÇÃO DA POSIÇÃO)
def update_figure(pais):
    ## Pega os dados para usar nos eixos do gráfico
    anos = ['2015', '2016', '2017', '2018', '2019']
    rankings = []
    for index, row in positionVar.iterrows():
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

    ## Retorna o gráfico
    return fig

# GRÁFICO CRISTIANO
# Alocação de dados nas variáveis a serem utilizadas posteriormente para o cálculo do percentual
rank_pais = crisDash['Country or region']
renda = crisDash['GDP per capita']
pontos = crisDash['Score']
suporte_social = crisDash['Social support']
saude = crisDash['Healthy life expectancy']
liberdade = crisDash['Freedom to make life choices']
generosidade = crisDash['Generosity']
corrupcao = crisDash['Perceptions of corruption']

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
  
  fig = px.line(x = rank_pais, y = razao, title = f'Variável utilizada:{variaveis}', template='plotly_white')
  fig.update_traces(name=f'{variaveis}', mode='lines+markers', line=dict(color='#3EECAC', width=3), marker=dict(color='#EE74E1', size=10))
  fig.update_yaxes(title = 'Percentual',showgrid= False)
  fig.update_xaxes(title = 'País/Região',showgrid= False)
  fig.update_layout(font_family='Poppins', font_color='#666', title_font_family='Poppins', title_font_color='#666', title_font_size=20, title_x=0.5, title_y=0.95, title_xanchor='center', title_yanchor='top', paper_bgcolor='#F5F5F5', plot_bgcolor='#c8c8c8')

  return fig

# Geração do gráfico
fig = calculo('Renda')

app.layout = html.Div(children=[
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
    dcc.Graph(
      id='grafico', 
      figure=fig,
      style={'borderRadius': '20px', 'width': '100%', 'margin': '0 auto', 'display': 'block'})                               
  ],style={'background': '#F5F5F5'})

@app.callback(
    dash.dependencies.Output('grafico','figure'),
    dash.dependencies.Input('Escolha','value')
)

def muda_grafico(value):
  fig = calculo(value)
  return fig


# GRÁFICO BRUNO

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

# Importando e atribuindo às variáveis as colunas necessárias para realizar o gráfico
df = pd.read_csv("C:\ProjetosVSCode\Python\Test\data\BrunoData.csv", sep=',')
pontuacao = df[variavel]
paises = df['Country']
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
def gera_grafico():
  fig = px.choropleth(
  locationmode = 'country names',
  locations = paises, 
  color = haver_paises, 
  hover_name = continentes, 
  projection = 'natural earth',
  color_continuous_scale = px.colors.sequential.Plasma,
  title = 'Média de felicidade por continente'
  )

  return fig

# A função vai mostrar a média por continente de cada variável
fig = gera_media_continente('Score')

opcoes = ['Score','GDP per capita', 'Social support', 'Healthy life expectancy', 'Freedom to make life choices', 'Generosity', 'Perceptions of corruption']

app.layout = html.Div(children=[
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
    dcc.Graph(
    id='grafico_continente',
    figure=fig,
    style={'borderRadius': '20px', 'width': '100%', 'margin': '0 auto', 'display': 'block'}
    )
], style={'background': '#F5F5F5'})

@app.callback(
    dash.dependencies.Output('grafico_continente','figure'),
    dash.dependencies.Input('op_variaveis', 'value')
)

def altera_grafico(value):
  fig = gera_media_continente(value)
  return fig

# Executa o dashboard
if __name__ == '__main__':
    app.run_server(debug=True)

import pandas as pd
import plotly.express as px
import dash
from dash import dcc
from dash import html

# Lê o arquivo csv
df=pd.read_csv("C:\ProjetosVSCode\Python\Test\data\AllSheets.csv", sep=',')

# Inicializa o dashboard
app = dash.Dash(__name__, external_stylesheets=['https://fonts.googleapis.com/css2?family=Poppins:wght@200;300;400;500;600;700;800;900&display=swap'])

# Filtra os dados para usar no dropdown
df = df[df["Country"].notnull()]
optionsCountry = [{"label": pais, "value": pais} for pais in df['Country'].unique()]

# Layout do dashboard com o dropdown para selecionar o país
app.layout = html.Div([
    html.Div(
    style={'display': 'flex', 'alignItems': 'center', 'justifyContent': 'center',},
    children=[html.H1('Dashboard da Felicidade', style={'fontFamily': 'Poppins', 'textAlign': 'center', 'fontSize': '2.5rem', 'background': '-webkit-linear-gradient(19deg, #EE74E1, #3EECAC 80%)','-webkit-background-clip': 'text','-webkit-text-fill-color': 'transparent', 'margin': '0'}),

    html.H1('😄', style={'fontFamily': 'Poppins', 'textAlign': 'center', 'fontSize': '2.5rem', 'marginLeft': '0.5rem','margin': '0'})]),

    html.H3('Selecione um país para ver a variação da posição no ranking da felicidade:', style={'fontFamily': 'Poppins', 'textAlign': 'center', 'fontSize': '1.5rem', 'background': '-webkit-linear-gradient(45deg, #EE74E1, #3EECAC 80%)','-webkit-background-clip': 'text','-webkit-text-fill-color': 'transparent'}),
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

# Callback para atualizar o gráfico de acordo com o país selecionado
@app.callback(
    dash.dependencies.Output('grafico-felicidade', 'figure'),
    dash.dependencies.Input('pais', 'value')
)

# Função para atualizar o gráfico
def update_figure(pais):
    ## Pega os dados para usar nos eixos do gráfico
    anos = ['2015', '2016', '2017', '2018', '2019']
    rankings = df[df['Country'] == pais]['Happiness Rank']

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

# Executa o dashboard
if __name__ == '__main__':
    app.run_server(debug=True)

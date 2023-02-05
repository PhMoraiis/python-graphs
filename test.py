import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output

df = pd.read_csv("C:\ProjetosVSCode\Python\Test\data\AllSheets.csv", sep=',')

def filter_data(df, country, years):
    filtered_df = df[df["Country"] == country]
    filtered_df = filtered_df[filtered_df["Year"].isin(years)]
    print(filtered_df)
    return filtered_df

def get_happiness_rank(df, country, years):
    filtered_df = filter_data(df, country, years)
    rank = filtered_df['Happiness Rank'].tolist()
    return rank


def update_graph(df, selected_country, selected_years):
    filtered_df = filter_data(df, selected_country, selected_years)
    rank = get_happiness_rank(df, selected_country, selected_years)
    fig = px.line(filtered_df, x='Year', y=rank, title="Variação da posição do país no ranking da felicidade")
    fig.update_traces(hovertemplate='<b>Ano: %{x}</b><br><b>Posição: %{y}</b>',hoverlabel=dict(bgcolor="white", font_size=16, font_family="Arial"))
    fig.update_traces(name='Variação da Posição', mode='lines+markers', line=dict(color='#666666', width=3), marker=dict(color='#000000', size=10))
    fig.update_yaxes(title='Posições no ranking', showgrid=True, gridcolor='#F3F3F3', titlefont=dict(family='Arial', size=16, color='#ffffff'))
    fig.update_xaxes(title='Anos', showgrid=True, gridcolor='#F3F3F3', titlefont=dict(family='Arial', size=16, color='#ffffff'))
    fig.update_layout(template='plotly_dark', paper_bgcolor='#272727', plot_bgcolor='#666666')
    return fig

external_stylesheets = ['C:\ProjetosVSCode\Python\Test\style.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df = df[df["Country"].notnull()]
options = [{"label": country, "value": country} for country in df["Country"].unique()]


app.layout = html.Div([
    html.H1("Variação da posição dos países no ranking da felicidade", style={'textAlign': 'center', 'color': '#272727', 'fontFamily': 'Arial', 'fontSize': '30px'}),
    html.Br(),
    html.Div("Selecione o país e os anos que deseja visualizar:", style={'textAlign': 'left', 'color': '#272727', 'fontFamily': 'Arial', 'fontSize': '20px'}),
    dcc.Dropdown(
        id='country-dropdown',
        options=options,
        value='Brazil',
        style={'width': '45%', 'textAlign': 'left', 'color': '#272727', 'fontFamily': 'Arial', 'margin': '10px 0'}
    ),
    dcc.Checklist(
        id='years-checklist',
        options=[
        {'label': '2015', 'value': 2015},
        {'label': '2016', 'value': 2016},
        {'label': '2017', 'value': 2017},
        {'label': '2018', 'value': 2018},
        {'label': '2019', 'value': 2019}
    ],
        value=[2015, 2016, 2017, 2018, 2019],
        style={'width': '30%', 'textAlign': 'left', 'color': '#272727', 'fontFamily': 'Arial'}
    ),
    html.Br(),
    dcc.Graph(id='happiness-graph'),
    html.Br()
])

@app.callback(
    Output('happiness-graph', 'figure'),
    [Input('country-dropdown', 'value'),
     Input('years-checklist', 'value')],
    
)

def update_figure(selected_country, selected_years):
    print(selected_country, selected_years)
    return update_graph(df, selected_country, selected_years)

app.run_server(debug=True)
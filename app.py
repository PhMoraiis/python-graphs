import pandas as pd
import plotly.express as px

df=pd.read_csv("C:\ProjetosVSCode\Python\Test\data\AllSheets.csv", sep=',')
# Importando os dados do arquivo CSV

valores_br = []
for i, row in df.iterrows():
    if row['Country'] == 'Brazil':
        valores_br.append(row)
# Realiza o filtro da linha do Brasil em cada ano, e adiciona em uma lista; O método iterrows() retorna o resultado do filtro da linha do Brasil, pegando todos os valores do Brasil independente das colunas, e adiciona em uma lista. Depois adiciona essa lista em outra lista, que será usada para criar o gráfico que é a "row".

rank=[]
for row in valores_br:
  rank.append(row['Happiness Rank']) 
# Agora pegando o valor do Happiness Rank da lista que foi iterada com todos os valores da linha do Brasil, filtra pela a coluna Happiness Rank e adiciona em uma lista chamada "rank".

dados_x= ['2015', '2016', '2017', '2018', '2019']
# Cria uma lista com os anos que serão usados no eixo X do gráfico.

dados_y=[rank]
# Cria uma lista com os valores do rank que será usada no eixo Y do gráfico.

fig = px.line(x=dados_x, y=dados_y, title='Variação da posição do Brasil no ranking da felicidade')
fig.update_traces(hovertemplate='<b>Ano: %{x}</b><br><b>Posição: %{y}</b>',hoverlabel=dict(bgcolor="white", font_size=16, font_family="Rockwell"))
fig.update_traces(name='Variação da Posição', mode='lines+markers', line=dict(color='#B0D236', width=3), marker=dict(color='#69BF54', size=10))
fig.update_yaxes(title='Posições no ranking')
fig.update_xaxes(title='Anos')
fig.show()
# Criando o gráfico

fig.write_html('C:\ProjetosVSCode\Python\Test\happiness_rank_brasil.html')
# Criando o arquivo HTML
import pandas as pd
import plotly.graph_objects as go

# Importando os dados dos arquivos CSV's

df1 = pd.read_csv('C:\ProjetosVSCode\Python\Test\data\Ano2015.csv', sep=',')
df2 = pd.read_csv('C:\ProjetosVSCode\Python\Test\data\Ano2016.csv', sep=',')
df3 = pd.read_csv('C:\ProjetosVSCode\Python\Test\data\Ano2017.csv', sep=',')
df4 = pd.read_csv('C:\ProjetosVSCode\Python\Test\data\Ano2018.csv', sep=',')
df5 = pd.read_csv('C:\ProjetosVSCode\Python\Test\data\Ano2019.csv', sep=',')

df1['Year'] = '2015'
df2['Year'] = '2016'
df3['Year'] = '2017'
df4['Year'] = '2018'
df5['Year'] = '2019'

df = pd.concat([df1, df2, df3, df4, df5])

# Filtrando os dados do Brasil

valores_br = []
for i, row in df.iterrows():
    if row['Country'] == 'Brazil':
        valores_br.append(row)

# Agora pegando o valor do Happiness Rank de cada ano

happiness_rank = []
for row in valores_br:
    happiness_rank.append(row['Happiness Rank'])

# Criando um novo dataframe com os dados apenas do Brasil contendo o ano e o Happiness Rank

df_br = []
for i in range(len(valores_br)):
    df_br.append([valores_br[i]['Year'], happiness_rank[i]])

# Criando o gráfico

fig = go.Figure(data=go.Scatter(x=[row[0] for row in df_br], y=[row[1] for row in df_br]))
fig.update_layout(title='Happiness Rank do Brasil', xaxis_title='Ano', yaxis_title='Happiness Rank')
fig.show()

# Criando o arquivo HTML

fig.write_html('C:\ProjetosVSCode\Python\Test\happiness_rank_brasil.html')
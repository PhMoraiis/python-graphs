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
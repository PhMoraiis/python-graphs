import pandas as pd

def concat_order(lista_arq, ordena_por):
    # Criando uma lista vazia para receber os dataframes
    lista_df = []
    
    # Lendo os arquivos e adicionando ao dataframe
    for file in lista_arq:
        df = pd.read_csv(file)
        df = df.sort_values(ordena_por, ascending=False)
        lista_df.append(df)
        
    # Concatenando os dataframes
    df = pd.concat(lista_df)
    return df

# Como usar
## lista_arq = ['file1.csv', 'file2.csv', 'file3.csv']
## df = concat_order(lista_arq, "ranking")

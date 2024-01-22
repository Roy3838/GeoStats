import pandas as pd


def get_alcohol(file_path):
    try:
        loaded_data = pd.read_csv(file_path, encoding='latin1', low_memory=False)
    except Exception as e:
        print(f"Error reading the file: {e}")
        return pd.DataFrame()  # Return an empty dataframe in case of an error

    filtered_NL_data = DF_only_NL(loaded_data)
    data = filtered_NL_data.copy()

    # Normalizar
    data['nom_estab'] = data['nom_estab'].apply(lambda x: normalize_text(x) if isinstance(x, str) else x)
    data['raz_social'] = data['raz_social'].apply(lambda x: normalize_text(x) if isinstance(x, str) else x)
    data['nombre_act'] = data['nombre_act'].apply(lambda x: normalize_text(x) if isinstance(x, str) else x)

    # Todo a minusculas
    data['nom_estab'] = data['nom_estab'].str.lower()
    data['raz_social'] = data['raz_social'].str.lower()
    data['nombre_act'] = data['nombre_act'].str.lower()

    # Lista de términos relacionados con la venta de alcohol
    terminos_alcohol = ['alcohol', 'licor', 'cerveza', 'bar', 'cantina', 'vinos', 'bebidas alcohólicas']

    # Existen estas columnas que clasificaremos
    columnas_a_clasificar = ['nombre_act', 'raz_social', 'nom_estab']

    # Lista para almacenar DataFrames filtrados
    filtered_dfs = []

    # Clasificamos los establecimientos por cada columna
    for columna in columnas_a_clasificar:
        # Filtramos y añadimos a la lista
        filtered_df = data[data[columna].str.contains('|'.join(terminos_alcohol), case=False, na=False)]
        filtered_dfs.append(filtered_df)

    # Combinamos todos los DataFrames filtrados
    combined_df = pd.concat(filtered_dfs).drop_duplicates()

    return combined_df


def main(paths = [
        '/home/jay/repos/AI/feminicidios/denue_00_46111_csv/conjunto_de_datos/denue_inegi_46111_.csv',
        '/home/jay/repos/AI/feminicidios/denue_00_46112-46311_csv/conjunto_de_datos/denue_inegi_46112-46311_.csv',
        '/home/jay/repos/AI/feminicidios/denue_00_46321-46531_csv/conjunto_de_datos/denue_inegi_46321-46531_.csv',
        '/home/jay/repos/AI/feminicidios/denue_00_46591-46911_csv/conjunto_de_datos/denue_inegi_46591-46911_.csv',
        
        # Sin querer puse el de las escuelas, xd que bueno que despues de get_alcohol() el DF estaba vacio
        #'/home/jay/repos/AI/feminicidios/denue_00_61_csv/conjunto_de_datos/denue_inegi_61_.csv'
        ]):
    # Iniciar un dataframe vacío
    combined_df = pd.DataFrame()

    # Iterar sobre cada ruta de archivo y aplicar la función get_alcohol
    for path in paths:
        df = get_alcohol(path)
        # Concatenar el dataframe actual al dataframe combinado
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    final_data = DF_to_float(combined_df)
    
    
    return final_data

    

if __name__ == "__main__":
    import matplotlib.pyplot as plt
    from utilities import *
    # Lista de rutas de archivos
    filtered_df = main()
    # Creating the scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(filtered_df['longitud'], filtered_df['latitud'], alpha=0.5)
    plt.title('Scatter Plot of Alcohol Selling Establishments')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()


else:
    from scripts.utilities import *

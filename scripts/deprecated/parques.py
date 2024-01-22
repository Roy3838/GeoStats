import pandas as pd


# Variables que codifican informacion 
""" 

Los principales identificadores de los establecimientos son:
        nom_estab, raz_social, nombre_act

        
Si alguno de estos identificadores contienen los terminos:
['parques', 'jardin', 'plaza', 'bosque', ''] -> Parques
"""


def main(file_path):
    try:
        loadeddata = pd.read_csv(file_path, encoding='latin1', low_memory=False)
    except Exception as e:
        print(f"Error leyendo el archivo: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error

    data = DF_only_NL(loadeddata)

    # Crear una copia del DataFrame para evitar el SettingWithCopyWarning
    data = data.copy()

    # Normalizar el resto de la data
    data['nom_estab'] = data['nom_estab'].apply(lambda x: normalize_text(x) if isinstance(x, str) else x)
    data['raz_social'] = data['raz_social'].apply(lambda x: normalize_text(x) if isinstance(x, str) else x)
    data['nombre_act'] = data['nombre_act'].apply(lambda x: normalize_text(x) if isinstance(x, str) else x)

    # Cambiar nombres para quitar mayúsculas
    data['nom_estab'] = data['nom_estab'].str.lower()
    data['raz_social'] = data['raz_social'].str.lower()
    data['nombre_act'] = data['nombre_act'].str.lower()

    # Vamos a clasificar los establecimientos en sector privado, sector público y hospitales
    terminos_parques = ['parques', 'jardin', 'plaza', 'bosque']

    # Existen estas columnas que clasificaremos
    columnas_a_clasificar = ['nombre_act', 'raz_social', 'nom_estab']

    # Lista para almacenar DataFrames filtrados
    filtered_dfs = []

    # Clasificamos los establecimientos por cada columna
    for columna in columnas_a_clasificar:
        # Filtramos y añadimos a la lista
        filtered_df = data[data[columna].str.contains('|'.join(terminos_parques), case=False, na=False)]
        filtered_dfs.append(filtered_df)

    # Combinamos todos los DataFrames filtrados
    combined_df = pd.concat(filtered_dfs).drop_duplicates()

    # Cambianos coordenadas a float
    combined_df = DF_to_float(combined_df)

    return combined_df
        





if __name__ == "__main__":

    import matplotlib.pyplot as plt
    from utilities import *

    # alcohol_establishments = compute_alcohol()
    file_path = '/home/jay/repos/GeoStats/denue/denue_00_71_csv/conjunto_de_datos/denue_inegi_71_.csv'
    # Creating the scatter plot
    plt.figure(figsize=(10, 6))
    salud = main(file_path)
    plt.scatter(salud['longitud'], salud['latitud'], alpha=0.5)
    plt.title('Parques')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

else:
    from scripts.utilities import *

    

import pandas as pd


# Variables que codifican informacion 
""" 

Los principales identificadores de los establecimientos son:
        nom_estab, raz_social, nombre_act

        
Si alguno de estos identificadores contienen los terminos:
['consultorio','privado', ''] -> Sector privado

['publico', 'imss', 'isste'] -> Sector Publico

['Hospital', 'Cirugia'] -> Hospital


Rechazamos los terminos:
['Comedor', 'Laboratorio', 'Estancias', 'Dentista', ''] -> No son establecimientos de salud
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

    # Lista de términos que vamos a filtrar que no son de salud
    terminos_no = ['comedor', 'laboratorio', 'estancias', 'dentista']
    # Quitar los términos que no son de salud
    data = data[~data['nombre_act'].str.contains('|'.join(terminos_no), case=False, na=False)]

    # Vamos a clasificar los establecimientos en sector privado, sector público y hospitales
    terminos_privados = ['consultorio', 'privado']
    terminos_publicos = ['público', 'imss', 'isste']
    terminos_hospitales = ['hospital', 'cirugía']

    # Existen estas columnas que clasificaremos
    columnas_a_clasificar = ['nombre_act', 'raz_social', 'nom_estab']

    # Creamos una columna que clasifique los establecimientos 
    data['sector'] = 'otro'

    # Clasificamos los establecimientos
    for columna in columnas_a_clasificar:
        data.loc[data[columna].str.contains('|'.join(terminos_privados), case=False, na=False), 'sector'] = 'privado'
        data.loc[data[columna].str.contains('|'.join(terminos_publicos), case=False, na=False), 'sector'] = 'público'
        data.loc[data[columna].str.contains('|'.join(terminos_hospitales), case=False, na=False), 'sector'] = 'hospital'

    # Cambiar coordenadas a float
    final_data = DF_to_float(data)
    
    return final_data




if __name__ == "__main__":

    import matplotlib.pyplot as plt
    from utilities import *

    # alcohol_establishments = compute_alcohol()
    file_path = '/home/jay/repos/GeoStats/denue/denue_00_62_csv/conjunto_de_datos/denue_inegi_62_.csv'
    # Creating the scatter plot
    plt.figure(figsize=(10, 6))
    salud = main(file_path)
    plt.scatter(salud['longitud'], salud['latitud'], alpha=0.5)
    plt.title('Scatter Plot of Alcohol Selling Establishments')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

else:
    from scripts.utilities import *

    

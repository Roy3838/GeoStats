import pandas as pd
import matplotlib.pyplot as plt
import unicodedata

def normalize_text(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

def main(file_path):
    try:
        data = pd.read_csv(file_path, encoding='latin1', low_memory=False)
    except Exception as e:
        print(f"Error reading the file: {e}")
        return pd.DataFrame()  # Return an empty dataframe in case of an error

    # Como Nuevo Leon tiene acento, se normaliza el texto para que no haya problemas
    data['entidad'] = data['entidad'].apply(lambda x: normalize_text(x) if isinstance(x, str) else x)

    # Normalizar el resto de la data
    data['nom_estab'] = data['nom_estab'].apply(lambda x: normalize_text(x) if isinstance(x, str) else x)
    data['raz_social'] = data['raz_social'].apply(lambda x: normalize_text(x) if isinstance(x, str) else x)
    data['nombre_act'] = data['nombre_act'].apply(lambda x: normalize_text(x) if isinstance(x, str) else x)

    # Cambiar nombres para quitar mayusculas
    data['nom_estab'] = data['nom_estab'].str.lower()
    data['raz_social'] = data['raz_social'].str.lower()
    data['nombre_act'] = data['nombre_act'].str.lower()

    # Lista de términos que vamos a filtrar que no son
    terminos_no = ['comedor', 'laboratorio', 'estancias', 'dentista']

    # Quitar los terminos que no de la data
    data = data[~data['nombre_act'].str.contains('|'.join(terminos_no), case=False, na=False)]

    # Vamos a clasificar los establecimientos en sector privado, sector publico y hospitales
    # Sector privado,
    terminos_privados = ['consultorio', 'privado']

    # Sector Publico,
    terminos_publicos = ['publico', 'imss']

    # Hospitales
    terminos_hospitales = ['hospital', 'cirugia']

    # Crear una columna para clasificar los establecimientos
    data['sector'] = 'otro'

    # Clasificar los establecimientos
    data.loc[data['nombre_act'].str.contains('|'.join(terminos_privados), case=False, na=False), 'sector'] = 'privado'
    data.loc[data['nombre_act'].str.contains('|'.join(terminos_publicos), case=False, na=False), 'sector'] = 'publico'
    data.loc[data['nombre_act'].str.contains('|'.join(terminos_hospitales), case=False, na=False), 'sector'] = 'hospital'


    filtered_df = data.dropna(subset=['latitud', 'longitud'])

    filtered_df['latitud'] = pd.to_numeric(filtered_df['latitud'], errors='coerce')
    filtered_df['longitud'] = pd.to_numeric(filtered_df['longitud'], errors='coerce')
    final_data = filtered_df.dropna(subset=['latitud', 'longitud'])


    return final_data

# Variables que codifican informacion 
""" Sector privado, 
nom_estab, raz_social, nombre_act

['consultorio','privado', '']





    Sector Publico, 
['publico', 'IMSS', '']

    


    Hospitales
['Hospital', 'Cirugia']


NO 

['Comedor', 'Laboratorio', 'Estancias', 'Dentista', '']


"""



if __name__ == "__main__":
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

    

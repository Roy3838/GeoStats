import pandas as pd
import matplotlib.pyplot as plt
import unicodedata

def normalize_text(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')

def get_alcohol(file_path):
    try:
        data = pd.read_csv(file_path, encoding='latin1', low_memory=False)
    except Exception as e:
        print(f"Error reading the file: {e}")
        return pd.DataFrame()  # Return an empty dataframe in case of an error

    # Como Nuevo Leon tiene acento, se normaliza el texto para que no haya problemas
    data['entidad'] = data['entidad'].apply(lambda x: normalize_text(x) if isinstance(x, str) else x)

    # Lista de términos relacionados con la venta de alcohol
    terminos_alcohol = ['alcohol', 'licor', 'cerveza', 'bar', 'cantina', 'vinos', 'bebidas alcohólicas']

    # Este es el filtro
    establecimientos_alcohol = data[data['nombre_act'].str.contains('|'.join(terminos_alcohol), case=False, na=False) & 
                                    (data['entidad'] == 'Nuevo Leon')]

    # regresa las cosas importantes y id para debuggear
    establecimientos_alcohol = establecimientos_alcohol[['id', 'nom_estab', 'nombre_act', 'latitud', 'longitud']]
    return establecimientos_alcohol


def main():
    # Lista de rutas de archivos
    paths = [
        '/home/jay/repos/AI/feminicidios/denue_00_46111_csv/conjunto_de_datos/denue_inegi_46111_.csv',
        '/home/jay/repos/AI/feminicidios/denue_00_46112-46311_csv/conjunto_de_datos/denue_inegi_46112-46311_.csv',
        '/home/jay/repos/AI/feminicidios/denue_00_46321-46531_csv/conjunto_de_datos/denue_inegi_46321-46531_.csv',
        '/home/jay/repos/AI/feminicidios/denue_00_46591-46911_csv/conjunto_de_datos/denue_inegi_46591-46911_.csv',
        
        # Sin querer puse el de las escuelas, xd que bueno que despues de get_alcohol() el DF estaba vacio
        '/home/jay/repos/AI/feminicidios/denue_00_61_csv/conjunto_de_datos/denue_inegi_61_.csv'
    ]

    # Iniciar un dataframe vacío
    combined_df = pd.DataFrame()

    # Iterar sobre cada ruta de archivo y aplicar la función get_alcohol
    for path in paths:
        df = get_alcohol(path)
        # Concatenar el dataframe actual al dataframe combinado
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    print(combined_df)

    # Filters
    filtered_df = combined_df.dropna(subset=['latitud', 'longitud'])

    filtered_df['latitud'] = pd.to_numeric(filtered_df['latitud'], errors='coerce')
    filtered_df['longitud'] = pd.to_numeric(filtered_df['longitud'], errors='coerce')
    filtered_df = filtered_df.dropna(subset=['latitud', 'longitud'])
    
    
    return filtered_df

    

if __name__ == "__main__":
    filtered_df = main()
    # Creating the scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(filtered_df['longitud'], filtered_df['latitud'], alpha=0.5)
    plt.title('Scatter Plot of Alcohol Selling Establishments')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

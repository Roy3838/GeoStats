import pandas as pd
from scripts.utilities import *

def filtrar_dataframe(ruta_archivo, columnas_para_filtrar, terminos_filtro):
    try:
        datos_cargados = pd.read_csv(ruta_archivo, encoding='latin1', low_memory=False)
    except Exception as e:
        print(f"Error al leer el archivo: {e}")
        return pd.DataFrame()  # Devuelve un DataFrame vacío en caso de error

    datos = DF_only_NL(datos_cargados)  # Asumiendo que DF_only_NL es una función predefinida

    # Crear una copia del DataFrame para evitar el SettingWithCopyWarning
    datos = datos.copy()

    # Normalizar los datos
    for columna in datos.columns:
        if columna in columnas_para_filtrar:
            datos[columna] = datos[columna].apply(lambda x: normalize_text(x) if isinstance(x, str) else x)
            datos[columna] = datos[columna].str.lower()

    # Si terminos_filtro está vacío, no se filtra por términos
    if terminos_filtro:
        # Filtrar el DataFrame
        dfs_filtrados = []
        for columna in columnas_para_filtrar:
            df_filtrado = datos[datos[columna].str.contains('|'.join(terminos_filtro), case=False, na=False)]
            dfs_filtrados.append(df_filtrado)

        # Combinar todos los DataFrames filtrados
        datos = pd.concat(dfs_filtrados).drop_duplicates()
    else:
        # Si terminos_filtro está vacío, usa el DataFrame como está
        datos = datos

    # Asumiendo que DF_to_float es una función predefinida
    datos = DF_to_float(datos)

    return datos


import pandas as pd
import unicodedata

"""
Script de utilidades para el proyecto de feminicidios
"""


# Normaliza un texto, si hay acentos o enyes, los quita
def normalize_text(text):
    return unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')


# Las coordenas vienen como string, las convertimos a float
def DF_to_float(data):

    filtered_df = data.dropna(subset=['latitud', 'longitud'])

    filtered_df['latitud'] = pd.to_numeric(filtered_df['latitud'], errors='coerce')
    filtered_df['longitud'] = pd.to_numeric(filtered_df['longitud'], errors='coerce')
    final_data = filtered_df.dropna(subset=['latitud', 'longitud'])

    return final_data


def DF_only_NL(data):

    # Como Nuevo Leon tiene acento, se normaliza el texto para que no haya problemas
    data['entidad'] = data['entidad'].apply(lambda x: normalize_text(x) if isinstance(x, str) else x)
    # Minusculas en entidad
    data['entidad'] = data['entidad'].str.lower()
    # Solo agarrar Nuevo Leon
    final_data = data[data['entidad'] == 'nuevo leon']

    return final_data

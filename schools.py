import pandas as pd
import matplotlib.pyplot as plt
from alcohol import main as compute_alcohol
from alcohol import normalize_text

def main():
    file_path = '/home/jay/repos/AI/feminicidios/denue_00_61_csv/conjunto_de_datos/denue_inegi_61_.csv'

    try:
        data = pd.read_csv(file_path, encoding='latin1', low_memory=False)
    except Exception as e:
        print(f"Error reading the file: {e}")


    filtered_df = data.dropna(subset=['latitud', 'longitud'])

    filtered_df['latitud'] = pd.to_numeric(filtered_df['latitud'], errors='coerce')
    filtered_df['longitud'] = pd.to_numeric(filtered_df['longitud'], errors='coerce')
    schools = filtered_df.dropna(subset=['latitud', 'longitud'])
    return schools

if __name__ == "__main__":
    
    # alcohol_establishments = compute_alcohol()
    schools = main()

    print(schools)

    # Creating the scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(schools['longitud'], schools['latitud'], alpha=0.5)
    plt.title('Scatter Plot of Alcohol Selling Establishments')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()




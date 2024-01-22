import pandas as pd

def main(file_path='/home/jay/repos/AI/feminicidios/denue_00_61_csv/conjunto_de_datos/denue_inegi_61_.csv'):
    try:
        data = pd.read_csv(file_path, encoding='latin1', low_memory=False)
    except Exception as e:
        print(f"Error reading the file: {e}")

    data = DF_only_NL(data)

    schools = DF_to_float(data)

    return schools


# los imports son malisimos lo siento si estas aqui por favor no me mates

if __name__ == "__main__":

    import matplotlib.pyplot as plt
    from utilities import *

    # alcohol_establishments = compute_alcohol()
    schools = main()
    # Creating the scatter plot
    plt.figure(figsize=(10, 6))
    plt.scatter(schools['longitud'], schools['latitud'], alpha=0.5)
    plt.title('Scatter Plot of Alcohol Selling Establishments')
    plt.xlabel('Longitude')
    plt.ylabel('Latitude')
    plt.show()

else: 
    from scripts.utilities import *






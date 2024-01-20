import matplotlib.pyplot as plt
import pandas as pd
import unittest
from scripts.distance import find_nearest 
from scripts.schools import main as compute_schools
from scripts.alcohol import main as compute_alcohol
from scipy.spatial import KDTree


def find_nearest(row, tree, establishments):
    distance, index = tree.query([row['latitud'], row['longitud']])
    return establishments.iloc[index]['nom_estab'], distance

if __name__ == "__main__":
    print("Computing schools...")
    schools = compute_schools()  # Make sure you have a compute_schools() function defined
    print("Computing alcohol establishments...")
    alcohol_establishments = compute_alcohol()  # Make sure you have a compute_alcohol() function defined
    print("Computing nearest alcohol...")
    # Tree para aplicar busqueda 
    alcohol_tree = KDTree(alcohol_establishments[['latitud', 'longitud']])

    # simon
    schools['nearest_alcohol'], schools['distance_to_nearest_alcohol'] = zip(*schools.apply(lambda row: find_nearest(row, alcohol_tree, alcohol_establishments), axis=1))
    # Iterate through schools and calculate distance to nearest alcohol establishment
    for _, school_row in schools.iterrows():
        nearest_name, distance = find_nearest(school_row, alcohol_tree, alcohol_establishments)
        print(f"School: {school_row['nom_estab']}, Nearest Alcohol: {nearest_name}, Distance: {distance:.2f} meters")
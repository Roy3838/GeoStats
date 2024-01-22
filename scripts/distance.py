from scripts.deprecated.schools import main as compute_schools
from scripts.deprecated.alcohol import main as compute_alcohol
from scipy.spatial import KDTree


# deprecated, see ipynb

def find_nearest(row, tree, establishments):
    distance, index = tree.query([row['latitud'], row['longitud']])
    return establishments.iloc[index]['nom_estab'], distance


def main():
    # coso para ver distancias
    alcohol_tree = KDTree(alcohol_establishments[['latitud', 'longitud']])

    # simon
    schools['nearest_alcohol'], schools['distance_to_nearest_alcohol'] = zip(*schools.apply(lambda row: find_nearest(row, alcohol_tree, alcohol_establishments), axis=1))


if __name__ == "__main__":
    print("computing alcohol establishments...")
    alcohol_establishments = compute_alcohol()
    print("computing schools...")
    schools = compute_schools()
    print("computing nearest alcohol...")
    main()
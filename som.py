import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from minisom import MiniSom
import pickle
from sklearn.neighbors import NearestNeighbors


# Importing the dataset
df = pd.read_csv('data.csv')
scaler = StandardScaler()
df[df.columns[1:]] = scaler.fit_transform(df[df.columns[1:]])

# load the model
with open('som_model.pkl', 'rb') as infile:
    som = pickle.load(infile)

data = df.iloc[:,1:].values
# for each item in your dataset, find the best matching unit (BMU) in the SOM and use its coordinates as the encoded representation
encoded_data = np.array([som.winner(x) for x in df.iloc[:,1:].values])

n_neighbors = 5
# define the distance metric to use
distance_metric = 'euclidean' # or 'cosine', or other distance metrics supported by scikit-learn
# initialize the nearest neighbors model with the encoded data
model = NearestNeighbors(n_neighbors=n_neighbors, metric=distance_metric)
model.fit(encoded_data)

# function to return the nearest neighbors based on the provided data
def get_nearest_neighbors(exemple):
    # encode the data using the SOM
    encoded_random_item = som.winner(exemple.values)
    # find the k nearest neighbors for the encoded random item
    encoded_random_item = np.array(encoded_random_item)
    distances, indices = model.kneighbors(encoded_random_item.reshape(1, -1))
    # here we print the indices of the k nearest neighbors
    print(indices[0])
    # here we print the items corresponding to the indices of the k nearest neighbors
    print(data[indices[0]])
    # here we print the items corresponding to the indices of the k nearest neighbors from the original dataset df with their id
    print(df.iloc[indices[0], :]['id'])

# get the nearest neighbors for a random item in the dataset
get_nearest_neighbors(df.iloc[:,1:].sample(1))
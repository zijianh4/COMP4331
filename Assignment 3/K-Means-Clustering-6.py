#import libraries
import pandas as pd
import time
from matplotlib import pyplot as plt
import numpy as np
from copy import deepcopy

# read the data
data = pd.read_csv('/Users/huangzijian/Documents/COMP4331/assignment/Assignment_3/a3dataset.txt', header=None)
data = data.to_numpy()

# Number of clusters
k = 6
# Number of training data
n = data.shape[0]
# Number of features in the data
c = data.shape[1]

start = time.time()

# Generate random centers
mean = np.mean(data, axis = 0)
std = np.std(data, axis = 0)
centers = np.random.randn(k,c)*std + mean

centers_old = np.zeros(centers.shape) # to store old centers
centers_new = deepcopy(centers) # Store new centers

# array of cluster number and distances
clusters = np.zeros(n)
distances = np.zeros((n,k))

error = np.linalg.norm(centers_new - centers_old)

# When, after an update, the estimate of that center stays the same, exit loop
while error != 0:
    
    for i in range(k):
        distances[:,i] = np.linalg.norm(data - centers[i], axis=1)
    
    clusters = np.argmin(distances, axis = 1)
    
    centers_old = deepcopy(centers_new)
    
    for i in range(k):
        centers_new[i] = np.mean(data[clusters == i], axis=0)
    error = np.linalg.norm(centers_new - centers_old)

end = time.time()
colormap = np.array(['r', 'g', 'b', 'c', 'm', 'y'])
plt.scatter(data[:,0], data[:,1], s=7, c=colormap[clusters])
plt.show()

SSE = np.linalg.norm(distances.min(axis=1))
print(SSE)
print(str(end-start)+"s")
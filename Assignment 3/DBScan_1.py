import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import time

# read the data
data = pd.read_csv('/Users/huangzijian/Documents/COMP4331/assignment/Assignment_3/a3dataset.txt', header=None)
data = data.to_numpy()

Eps = 5
MinPts = 10  

start = time.time()

# build the neighbor table
Neighbor_table = {}
for i in range(data.shape[0]):
    cur_pts = data[i]
    distances = np.linalg.norm(data - cur_pts, axis=1)
    Neighbor_table[i] = np.where(distances<=Eps)[0]

# find the core points
core_pts = {}
for i in range(data.shape[0]):
    if len(Neighbor_table[i]) >= MinPts:
        core_pts[i] = Neighbor_table[i]

cluster = np.zeros(data.shape[0]).astype(np.int)
record = np.zeros(data.shape[0]).astype(np.int)

# DBSCAN function
def DB(core, k):
    cluster[core] = k
    record[core] = 1
    
    for i in core_pts[core]:
        if i in core_pts.keys():
            if record[i] == 0:
                DB(i, k)
        else:
            cluster[i] = k
    return

k = 1
for key in core_pts:
    if record[key] == 0:
        DB(key, k)
        k += 1

end = time.time()

# extract noises
noise_idx = np.where(cluster==0)[0]
noises = data[noise_idx]

plt.scatter(data[:,0], data[:,1], s=3, c=cluster)
plt.scatter(noises[:,0], noises[:,1], s=3, c='black')

print(str(end-start)+'s')
plt.show()


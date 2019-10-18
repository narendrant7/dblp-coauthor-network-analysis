import sys
from urllib.parse import quote
import pandas as pd
import pylab as plt
import matplotlib.pyplot as plt2

df = pd.read_csv('clus_dens.txt')
x = df.iloc[:,0]
y1 = df.iloc[:,1]
y2 = df.iloc[:,2]

plt.scatter(x, y2, color = 'red', zorder = 2)
plt.plot(x, y2, color = 'blue', zorder = 1)
plt.title('Clustering Coefficient by Years')
plt.xlabel('Year')
plt.ylabel('Clustering Coefficient')
plt.savefig('./output/graphs/Clus_Coeff.png')
plt.close()
print('Graph for Clustering Coefficient created')

axes = plt.gca()
axes.set_ylim([-0.0001,0.0005])
plt.scatter(x, y1, color = 'red', zorder = 2)
plt.plot(x, y1, color = 'blue', zorder = 1)
plt.title('Network Density by Years')
plt.xlabel('Year')
plt.ylabel('Network Density')
plt.savefig('./output/graphs/Net_Density.png')
plt.close()
print('Graph for Network Density created')

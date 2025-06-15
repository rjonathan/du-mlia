import matplotlib.pyplot as plt
import pandas as pd
import numpy as np



# ###################################
# Test import matplot
# ###################################
# fig, ax = plt.subplots()             # Create a figure containing a single Axes.
# ax.plot([1, 2, 3, 4], [1, 4, 2, 3])  # Plot some data on the Axes.
# plt.show()  


# ###################################
# Chargement des datas
# ###################################
data1 = pd.read_csv('./data/etudes-superieurs.csv',sep=';',  dtype={0: str})
print(data1.head())  # Print the first rows of the dataframe

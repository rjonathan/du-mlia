import pandas as pd


#from google.colab import drive
#drive.mount('/content/drive')

# ###################################
# Chargement des datas
# ###################################

# https://archive.ics.uci.edu/dataset/697/predict+students+dropout+and+academic+success

#dataEtudeSup = pd.read_csv('/content/drive/MyDrive/Colab Notebooks/du-mlia-code/data/etudes-superieurs.csv',sep=';',  dtype={0: str})
dataEtudeSup = pd.read_csv('./data/etudes-superieurs.csv',sep=';',  dtype={0: str})
dataEtudeSup.columns = dataEtudeSup.columns.str.strip()  # Enlève espaces et tabulations
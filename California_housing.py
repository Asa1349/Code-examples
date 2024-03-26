# ------------------------------------------------
# Dateiname: California_housing.py
# Version: 1.0
# Funktion: Schätzt den Wert eines Hauses in Kalifornien
# Autor: AP
# Datum der letzten Änderung: 24.10.2023
# ------------------------------------------------


# verwendete Module ------------------------------------------------------------

import pandas as pd
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
import urllib.request
from pathlib import Path

# Laden des Datensatzes -------------------------------------------------------

df = pd.read_csv("G:\Programmieren\Machine Learning\O'Reilly\data\housing.csv")


# Analyse der Daten -----------------------------------------------------------

# überprüfe Daten
print(
    df.info(), '\n\n',
    df['ocean_proximity'].value_counts(), '\n\n',
    df.describe(),'\n\n'
    )

# Ansicht der Daten als Histogramm
df.hist(bins=50, figsize=(12,8))


# Visualisierung der geografischen Daten
df_renamed = df.rename(columns={'latitude':'Latitude', 'longitude':'Longitude', 
                                'population':'Population', 'median_house_value':'Median house value (USD)'})

df_renamed.plot(kind='scatter', x='Longitude', y='Latitude', s=df_renamed['Population'] / 100, label='Population', 
                c='Median house value (USD)', cmap='jet', colorbar=True, legend=True, sharex=False, figsize=(10, 7))

map_img = plt.imread("G:\Programmieren\Machine Learning\O'Reilly\data\california_map_c.png")
axis = -124.55, -113.95, 32.45, 42.05
plt.axis(axis)
plt.imshow(map_img, extent=axis)
plt.title('Population and median house value in California')


# Ermittlung des Korrelationskoeffizienten von median_house_value zu den restlichen Merkmalen
corr_matrix = df.drop('ocean_proximity', axis=1).corr()
print('Korrelationskoeffizienten von median_house_value \n', corr_matrix['median_house_value'].sort_values(ascending=False), '\n\n')


# Erzeugung einer Scatterplot-Matrix 
attributes = ['median_house_value', 'median_income', 'total_rooms', 'housing_median_age']
scatter_matrix(df[attributes], figsize=(12,8))
plt.title('Scatterplot Matrix', loc='center')


# Erstellen eine Korrelationsmatrix mit aussagekräftigeren Merkmalen
df['rooms_per_house'] = df['total_rooms'] / df['households']
df['bedrooms_ratio'] = df['total_bedrooms'] / df['total_rooms']
df['people_per_house'] = df['population'] / df['households']
corr_matrix = df.drop('ocean_proximity', axis=1).corr()
print('Korrelationsmatrix mit aussagekräftigeren Merkmalen \n', corr_matrix['median_house_value'].sort_values(ascending=False),'\n\n')


# Aufbereitung der Daten -----------------------------------------------------------

# Fehlende Werte (z.B. in total_bedrooms) durch den Median ersetzen
imputer = SimpleImputer(strategy='median')
df_num = df.select_dtypes(include=[np.number])
X = imputer.fit_transform(df_num)
df_trans = pd.DataFrame(X, columns=df_num.columns, index=df_num.index)

# kategorische Merkmale in numerische Werte wandeln
df['ocean_proximity'] = df['ocean_proximity'].astype('category').cat.codes

df_labels = df.drop("median_house_value", axis=1)
df_targets = df["median_house_value"]

# Skalierung der Daten
target_scaler = StandardScaler()
scaled_labels = target_scaler.fit_transform(df_labels)

# generieren von Test- und Trainingsdaten
X_train, y_train, X_test, y_test = train_test_split(scaled_labels,df_targets,test_size=0.2, random_state=42)


model = LinearRegression().fit(X_train,y_train)
scaled_predictions = model.predict(X_test)
predictions = target_scaler.inverse_transform(scaled_predictions)

# Ausgabe ----------------------------------------------------------------------

# plt.show()


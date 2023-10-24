# ------------------------------------------------
# Dateiname: KNN and Decision Tree.py
# Version: 1.0
# Funktion: KNN
# Autor: AP
# Datum der letzten Änderung: 20.10.2023
# ------------------------------------------------

# verwendete Module ------------------------------------------------------------------------

import pandas as pd
import numpy as np
from sklearn import metrics
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV


# Aufbereitung der Daten -------------------------------------------------------------------

df = pd.read_csv('G:\Programmieren\Machine Learning\Übungen\data\MobilePhone.csv')

# wandelt strings in numerische Werte
df['Price Range'] = df['Price Range'].astype('category').cat.codes

# Daten auf Nullvalues überprüfen
# print(df.isnull().sum())

X = df.drop(columns='Price Range')
y = df['Price Range']

# Teilung in Test- und Trainingsdaten
X_train, X_test, y_train, y_test = train_test_split(X,y, test_size=0.25, random_state=5)


# KNN Model----------------------------------------------------------------------------------

# KNN Training
knn = KNeighborsClassifier(n_neighbors=5)
knn.fit(X_train, y_train)

# Test des Models und berechnen der Accuracy
y_pred_knn = knn.predict(X_test)
accuracy = metrics.accuracy_score(y_test, y_pred_knn)

# Cross Validation
knn_cv = KNeighborsClassifier(n_neighbors=5)
cv_scores = cross_val_score(knn_cv, X, y, cv=5)
cv_scores_mean = round(np.mean(cv_scores), 4)

# Bestimmung der besten Performance
knn_perf = KNeighborsClassifier()
param_grid = {'n_neighbors': np.arange(1,25)}
knn_gscv = GridSearchCV(knn_perf, param_grid, cv=5)
knn_gscv.fit(X, y)


# Decision Tree Model ------------------------------------------------------------------------

# Decision Tree training
tree = DecisionTreeClassifier().fit(X_train, y_train)

# Test des Models und berechnen der Accuracy
score_train = tree.score(X_train, y_train)
score_test = tree.score(X_test, y_test)

# Bestimmung der besten Performance
parameters = {'max_depth': [3,4,5,6,7], 'max_leaf_nodes': [2,3,4,5,6]}
tree_gscv = GridSearchCV(tree, parameters)
tree_gscv.fit(X_train, y_train)

# Test des Models und berechnen der Accuracy
score_train_gscv = tree_gscv.score(X_train, y_train)
score_test_gscv = tree_gscv.score(X_test, y_test)


# Ausgabe ------------------------------------------------------------------------------------

print('KNN Model')
print('---------------------------------------------')
print('Accuracy: ', accuracy)
print('Cross Validation Mean Score: ', cv_scores_mean)
print('Best performing n_neighbours value: ', knn_gscv.best_params_['n_neighbors'])
print('Mean score for the top performing value of n_neighbors: ', knn_gscv.best_score_)
print()
print()
print('Decisioin Tree Model')
print('---------------------------------------------')
print('Accuracy train set: ', score_train)
print('Accuracy test set: ', score_test)
print('GSCV Accuracy train set: ', score_train_gscv)
print('GSCV Accuracy test set: ', score_test_gscv)
print('Best performing parameters:', tree_gscv.best_params_)



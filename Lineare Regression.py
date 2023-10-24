# ------------------------------------------------
# Dateiname: Lineare Regression.py
# Version: 1.0
# Funktion: Funktionen zur Berechnung der Linearen Regression
# Autor:  AP
# Datum der letzten Änderung: 28.09.2023
# ------------------------------------------------


# Modulimport ---------------------------------------------------------------------------------------

import math
import numpy as np
import matplotlib.pyplot as plt


# Definition der Funktionen -------------------------------------------------------------------------

def standardabweichung(liste):
    '''Berechnet die Standardabweichung einer Liste'''
    mittelwert = sum(liste) / len(liste)
    varianz = sum((i - mittelwert)**2 for i in liste) / len(liste)
    abweichung = math.sqrt(varianz)
    return abweichung

def kovarianz(liste1, liste2):
    '''Berechnet die Kovarianz zweier Listen'''
    average_x = sum(liste1) / len(liste1)
    average_y = sum(liste2) / len(liste2)
    l_abweichungX = []                                  
    l_abweichungY = []                                  
    for x in liste1:                                     
        abweichungX = x - average_x                     
        l_abweichungX.append(abweichungX)               
    for y in liste2:
        abweichungY = y - average_y
        l_abweichungY.append(abweichungY)
    l_produktXY = [x * y for x,y in zip(l_abweichungX,l_abweichungY)]
    summe_produkte = sum(l_produktXY)
    kov = summe_produkte * 1/(len(liste1))
    return kov

def korrelation(liste1,liste2):
    '''Berechnet die Korrelation zweier Listen'''
    kor = kovarianz(liste1,liste2) / (standardabweichung(liste1) * standardabweichung(liste2))
    return kor

def regression(liste1,liste2):
    '''Berechnet die Regression zwieer Listen'''
    average_x = sum(liste1) / len(liste1)
    average_y = sum(liste2) / len(liste2)
    steigung = (standardabweichung(liste2) / standardabweichung(liste1)) * korrelation(liste1, liste2)
    y_achse = - (standardabweichung(liste2) / standardabweichung(liste1)) * korrelation(liste1,liste2) * average_x + average_y
    return steigung, y_achse

def vorhersage(data):
    '''Sagt bei Eingabe des x-Wertes einen y-Wert mittels Regression voraus'''
    steigung = regression(tagestemp,besucher) [0]
    y_achse = regression(tagestemp,besucher) [1]
    predict = steigung * data + y_achse
    return predict


# Ausgabe -------------------------------------------------------------------------------------------

# verwendete Daten
tagestemp = [28,23,32,35,29,30,27,34,32]
besucher = [400,60,630,660,420,590,376,620,612]

temp = 26

print('Bei einer Tagestemperatur von', temp, '°C werden', int(vorhersage(temp)), 'Besucher erwartet.')

#Plotten der Linearen Regression 
x = np.linspace(20,36,100)
plt.scatter(tagestemp,besucher)
plt.plot(x,vorhersage(x), c='purple')
plt.xlabel('Temperatur in °C')
plt.ylabel('Besucheranzahl')
plt.title('Lineare Regression zur Vorherbestimmung \n der Besucheranzahl bei Tagestemperatur')
plt.show()
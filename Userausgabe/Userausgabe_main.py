# ------------------------------------------------
# Dateiname: Userausgabe_main.py
# Version: 1.3
# Funktion: Ausgabe einer Userdatenbank in einer übersichtlichen Tabelle via Streamlit
# Autor: AP
# Datum der letzten Änderung: 19.09.2023
# ------------------------------------------------


# verwendete Module -----------------------------------------------------------------------

import streamlit as st
import pandas as pd



# Auslesen der Daten ---------------------------------------------------------------------------


with open(r'G:\Programmieren\Projekte\Userausgabe\daten\vshell_userdb.txt', 'r') as f:

    # Überspringt die erste Zeile
    f.readline()
                
    l_name = []
    l_passwort = []
    l_ID = []
    l_typ = []
    l_kommentar = []
    l_mitgliedschaft = []
    

    # gibt jede Zeile des Files als Liste aus, trennt die Elemente bei jedem ":"
    for line in f:
                line = line.strip()
                line = line.split(":")
                # fügt die Elemente den entsprechenden Listen hinzu
                l_name.append(line[0])
                l_passwort.append(line[1])
                l_ID.append(line[2])
                l_typ.append(line[3])
                l_kommentar.append(line[4])
                l_mitgliedschaft.append(line[5])
 

# Splittet die Strings im Falle mehrerer Gruppenzugehörigkeiten auf und gibt diese als Liste wieder.
# Speichert die Gruppenzugehörigleit(Gruppen-IDs) in einer neuen Liste, um die richtige Reihenfolge beizubehalten.
l_mitgliedschaften = []
for ids in l_mitgliedschaft:
    if "," in ids:
        l_mitgliedschaften.append((ids.split(",")))
    else:
        l_mitgliedschaften.append(ids)

# überprüft, ob ein Element in l_mitgliedschaften eine Liste ist.
# wenn ja, dann wird für jeden Eintrag in der Unterliste die entsprechende ID gesucht und der Name zugewiesen
l_gruppe = []
for element in l_mitgliedschaften:
    if type(element) is list:
        if element[0] in l_ID:
            i = l_ID.index(element[0])
            x = l_name[i]
        else:
            x = "unbekannt"
        if element[1] in l_ID:
            i = l_ID.index(element[1])
            y = l_name[i]
        else:
            y = "unbekannt"
        l_gruppe.append((x+" | "+y))
    # vergleicht die IDs aus l_mitgliedschaft mit l_ID und gibt den entsprechenden Index von l_ID aus, um den Namen aus l_name der Liste l_gruppe zuzuweisen
    elif element in l_ID:
        i = l_ID.index(element)
        l_gruppe.append(l_name[i])
    else:
        l_gruppe.append("")



# Ausgabe ---------------------------------------------------------------------------------


st.write("# Datenbank User und Gruppen")    
#erstellt eine Tabelle mit den Listen als Daten
df = pd.DataFrame(
    {
        "Name": l_name,
        "Passwort": l_passwort,
        "ID": l_ID,
        "Typ": l_typ,
        "Kommentar": l_kommentar,
        "Gruppe": l_gruppe
    }
)

st.dataframe(df)




    







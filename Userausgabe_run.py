# ------------------------------------------------
# Dateiname: Userausgabe_run.py
# Version: 1.0
# Funktion: Ausgabe der Datenbank in Streamlit
# Autor: AP
# Datum der letzten Änderung: 30.12.2023
# ------------------------------------------------

# verwendete Module -----------------------------------------------------------------------------

import subprocess


# auslesen des Hauptscriptes und generieren einer temporären Datei ------------------------------

# Pfad zur Hauptdatei
main_script_path = r'G:\Programmieren\Projekte\Userausgabe\Userausgabe_main.py'

# Erzeuge einen temporären Streamlit-Script-Dateinamen
streamlit_script_filename = "Userausgabe_temp.py"

# Lese den Inhalt der Hauptdatei
with open(main_script_path, 'r', encoding='utf-8') as main_script_file:
    main_script_content = main_script_file.read()

# Schreibe den Streamlit-Code in die temporäre Datei
with open(streamlit_script_filename, 'w', encoding='utf-8') as streamlit_script:
    streamlit_script.write(main_script_content)



# Start in Streamlit -----------------------------------------------------------------------------

if __name__ == "__main__":
    # Starte Streamlit als subprocess
    subprocess.run(["streamlit", "run", streamlit_script_filename])

    # Lösche die temporäre Streamlit-Script-Datei
    subprocess.run(["del", streamlit_script_filename], shell=True)






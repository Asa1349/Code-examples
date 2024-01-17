# ------------------------------------------------
# Dateiname: Galgenmännchen.py
# Version: 1.0
# Funktion: Galgenmännchen-Spiel
# Autor: AP
# Datum der letzten Änderung: 16.01.2024
# ------------------------------------------------

# verwendete Module --------------------------------------------------------------------------------------------

import random


# Definition der Funktionen ------------------------------------------------------------------------------------

def start():
    '''Start-Nachricht mit Spielerklärung und Abfrage'''
    print('Willkommen zu Galgenmännchen!')
    gallows(gallows_empty)
    print('|~~~|~~~|~~~|~~~|~~~|\n')
    print('Galgenmännchen ist ein Spiel, in dem Wörter erraten werden müssen.')
    print('Bei jeder falschen Eingabe füllt sich der Galgen und führt bei nicht')
    print('rechtzeitigem Erraten des Wortes zum Tode des Galgenmännchens.')
    print('Die Eingabe erfolgt in einzelnen Kleinbuchstaben.')
    print('Bist du schlau und schnell genug um dem Ende durch den Galgen zu entgehen?')
    print('Wir werden sehen....\n')
    start_input = input('(S)tarten oder (b)eenden?  ')
    print()
    if start_input in ['s', 'S']:
        print('Viel Spaß!\n\n')
        game()
    elif start_input in ['b', 'B']:
        print('Ohje, zu schwache Nerven... \n')
        quit()
    else:
        print('ungültige Eingabe! \n')
        start_input = input('(S)tarten oder (b)eenden?  ')
        print()
                

def gallows(empty_gallows):
    '''Zeichnung des Galgen'''
    print(
        ' ______________','\n',
        ' |          '+ gallows_empty[0],'\n',
        ' |         '+ gallows_empty[1],'\n',
        ' |          '+ gallows_empty[2],'\n',
        ' |         '+ gallows_empty[3] + gallows_empty[2] + gallows_empty[4],'\n',
        ' |         '+ gallows_empty[5] + ' ' + gallows_empty[6],'\n',
        ' |             ','\n',
        '/ \\',
        '\n'
    )


def status():
    '''Ausgabe des zu ratenden Wortes mit Buchstaben oder Füllzeichen'''
    print('Wort:')
    for letter in word:
        if letter.lower() in l_answer:
            print(letter, end=' ')
        elif letter.isalpha():
            print('_', end=' ')
    print()


def game():
    '''Spieldurchlauf mit Gewinnbedingung'''
    # solange die Lösung nicht dem Wort entspricht wird weiter geraten
    while set(l_answer) != set(l_word):
        status()
        print()
        entry = input("Rate: ").lower()
        print()
        # überprüft, ob auch nur ein Buchstabe eingegeben wurde
        if len(entry) != 1 or not entry.isalpha():
            print('Nur einen Buchstaben eingeben!')
            continue

        # richtiger Buchstabe - Buchstabe wird zur Lösung hinzugefügt
        if entry in l_word:
            print("Richtig! \n")
            l_answer.append(entry)
            
        # falscher Buchstabe - der Fehlerzähler wird um 1 erhöht und das entsprechende Symbol im Galgen gezeigt
        else:
            print("Falsch! \n")
            global error
            error += 1
            if error <= 6:
                # das Symbol aus gallows full wird in gallows_empty geschrieben
                gallows_empty[error] = gallows_full[error]
                # der aktuelle Galgen wird ausgegeben
                gallows(gallows_empty)  
            else:
                break

    # Gewinnbedingung    
    if set(l_answer) == set(l_word):
        global wins
        print()
        print("Gewonnen! Das Wort lautet: ", word, '\n')
        print('Gerade noch dem Galgen entkommen... kein Festmahl für die Krähen heute... schade... \n')
        wins += 1
        print('Aktuelle Punktzahl: ', wins, '\n')
        new_game()
        
    else:
        print()
        print("Verloren! Das Wort lautet: ", word, '\n')
        print('Welch Jammer... Irgendwelche letzten Worte? Muhahaha... \n')
        print('Aktuelle Punktzahl: ', wins, '\n')
        new_game()        


def new_game():
    '''Start eines neuen Spieldurchlaufs und Rücksetzen des Galgen und Wortes'''
    global error
    global gallows_empty
    global l_answer
    global l_word
    global word
    new_input = input('Willst Du das Schicksal ein weiteres Mal herausfordern?   (j)a / (n)ein   \n')
    if new_input in ['j', 'J']:
        # Wort und Galgen werden zurückgesetzt
        word = random.choice(words)
        l_word = list(word.lower())
        l_answer = []
        error = -1
        gallows_empty = [' ', ' ', ' ',  ' ', ' ', ' ', ' ']
        print('Auf ein Neues... \n')
        game()
    elif new_input in ['n', 'N']:
        quit()
    else:
        print('ungültige Eingabe! \n')
        new_input = input('Willst Du das Schicksal ein weiteres Mal herausfordern?   (j)a / (n)ein   \n')


# Definition der Variablen -------------------------------------------------------------------------------------

# Definition der Wortliste
words = ['Python','Javascript','Compiler','Funktion','Programmiersprachen','Objektorientiert']

# sucht ein beliebiges Wort aus der Liste zum Raten
word = random.choice(words)

# zur vereinfachung werden alle wörter in Kleinbuchstaben umgewandelt
l_word = list(word.lower())
# erstellt eine leere Liste in der die richtig geratenen Buchstaben augenommen werden
l_answer = []

# Symbole für den leeren bzw. vollen Galgen
gallows_empty = [' ', ' ', ' ',  ' ', ' ', ' ', ' ']
gallows_full = ['|', '( )', '|', '/', '\\', '/', '\\']

# Fehlerzähler
error = -1

# Punktezähler
wins = 0

# Spielstart -----------------------------------------------------------------------------------------------------

start()
   
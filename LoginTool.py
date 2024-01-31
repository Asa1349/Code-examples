# ------------------------------------------------
# Dateiname: LoginTool.py
# Version: 1.1
# Funktion: Login auf Webseite, Auslesen der Login-Zeit, Wiederholte Anmeldung in vorgegebenen Zeitraum
# Autor: AP
# Datum der letzten Änderung: 30.12.2023
# ------------------------------------------------

# verwendete Module ------------------------------------------------------------------------------------------------------

import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from datetime import datetime, date


# Auslesen der Login Daten ------------------------------------------------------------------------------------------------

with open('login.txt', 'r') as f:
    lines = f.readlines()

driverpath = lines[0].strip()
website_url = lines[1].strip()
username = lines[2].strip()
password = lines[3].strip()




# Definition der Funktionen ----------------------------------------------------------------------------------------------

def login():
    '''Führt den Login auf der Webseite durch, navigiert zu gewissen Menüpunkten und liest die Zeit des letzten Logins aus.'''

    # Hier wird Firefox als Browser verwendet, dieser Teil muss für Chrome oder andere Browser entsprechend angepasst werden
    options = webdriver.FirefoxOptions()
    # '--start-maximized' öffnet ein Browserfenster, für den Betrieb auf z.B. Linux-Server ohne GUI hier das Argument '--headless' verwenden 
    options.add_argument('--start-maximized') 
    service = webdriver.firefox.service.Service(executable_path=driverpath)
    driver = webdriver.Firefox(service=service, options=options)


    waiting_time = random.randint(45,70)*60
    

    print("Navigiere zur Webseite")
    time.sleep(5)
    driver.get(website_url)
    print("Wartezeit nach dem Laden der Seite")
    time.sleep(5)

    # Login auf Webseite
    print("Finde Benutzernamen-Element")
    username_input = driver.find_element(By.CSS_SELECTOR, '#username')
    print("Benutzernamen eingeben")
    username_input.send_keys(username)

    print("Finde Passwort-Element")
    password_input = driver.find_element(By.CSS_SELECTOR, '#password')
    print("Passwort eingeben")
    password_input.send_keys(password)

    print("Finde Login_Button-Element")
    login_button = driver.find_element(By.CSS_SELECTOR, '#loginbtn')
    print("Login_Button click")
    login_button.click()
    time.sleep(10)
    print("Login durchgeführt")


    # Aktionen, die auf der Webseite ausgeführt werden
    print("Finde Menü_Button-Element")
    menü_button = driver.find_element(By.XPATH, '/html/body/div[3]/nav/div[2]/div/div/div/a/span/span/span/span')
    print("Menü_Button click")
    menü_button.click()
    time.sleep(5)

    print("Finde Profil_Button-Element")
    profil_button = driver.find_element(By.XPATH, '/html/body/div[3]/nav/div[2]/div/div/div/div/div/div/div[1]/a[1]')
    print("Profil_Button click")
    profil_button.click()
    time.sleep(5)

    print("Finde login_time-Element")
    login_time_element = driver.find_element(By.XPATH, '/html/body/div[2]/div[3]/div[2]/div[2]/div/section/div/div/div/section[5]/div/ul/li[2]/dl/dd')
    print('login_time ausgelesen')
    time.sleep(2)
    login_time = login_time_element.text
    print(login_time)
    time.sleep(2)
   
    print("Finde Dashboard_Button-Element")
    dashboard_button = driver.find_element(By.XPATH, '/html/body/div[2]/nav/div[1]/nav/ul/li[2]/a')
    print("Dashboard_Button click")
    dashboard_button.click()
    time.sleep(5)

    
    # Zeigt die aktuelle Zeit, die Zeit des Logins und die random - Wartezeit
    current_time = datetime.now().time().strftime('%H:%M')
    print('Letzter Login: ', login_time)
    print('Aktuelle Zeit: ', current_time)
    print('Zeit bis zu erneutem Login: ', waiting_time/60, 'min')


    # Schließt das Fenster nach der random - Wartezeit
    time.sleep(waiting_time)
    driver.quit()
    print('Fenster geschlossen')



def check_login_time():
    '''Überprüft den Wochentag und das Zeitfenster, wann der Login durchgeführt werden soll.'''
    now_day = date.today()
    weekday = now_day.weekday()
    now_hour = time.localtime().tm_hour
    
    # Überprüfe, ob Wochenende ist
    if weekday in [5,6]:
        print("Es ist Wochenende!")
    # Überprüfe, ob die aktuelle Stunde zwischen 8.00 und 16.00 liegt
    elif 8 <= now_hour < 16:
        print("Es ist Zeit für den Login!")
        login()
    else:
        print("Es ist nicht Zeit für den Login.")
    
        


# Hauptprogramm -----------------------------------------------------------------------------------------------------------
        
if __name__ == "__main__":


    while True:
        # Überprüft das Zeitfenster
        check_login_time()
        # Wartezeit bis zur neuen Überprüfung
        time.sleep(600)

from flask import Blueprint, render_template, request, flash, redirect, session, Flask, url_for
from firebase_admin import firestore
import pyrebase

config = {
    'apiKey': "",
    'authDomain': "",
    'projectId': "",
    'storageBucket': "",
    'messagingSenderId': "",
    'appId': "",
    'measurementId': "",
    'databaseURL': ""
}

#auth.secret_key = 'wauuuu'

firebase = pyrebase.initialize_app(config)
prihlasovani = firebase.auth()
auth = Blueprint('auth', __name__)

@auth.route('prihlaseni', methods=['POST', 'GET'])
def login():
    if('uzivatel' in session): #Podmínky pro již pihlášeného uživatele
        return redirect(url_for('views.uzivatel')) #Přesměrování přihlášeného uživatele do aplikace
    if request.method == 'POST':
        e_mail = request.form.get('e_mail')
        heslo = request.form.get('heslo')
        try: #Pokus o přihlášeného
            uzivatel = prihlasovani.sign_in_with_email_and_password(e_mail,heslo) #Zjištění jestli je uživatel v databázi a jestli se email shoduje s heslem
            session['uzivatel'] = e_mail #Vytvoření sessionu, který je stejný jako email uživatele
            return redirect(url_for('views.uzivatel')) #Přesměrování přihlášeného uživatele do aplikace
        except: #Když se nepovede přihlášení
            flash('Nesprávné heslo, nebo uživatelské jméno', category='chyba') #Vyskakovací zpráva o chybě přihlášení
    return render_template("prihlaseni.html")
    #Hotovo pro Beta verzi :)


@auth.route('odhlaseni')
def logout():
    if('uzivatel' in session):
        session.pop('uzivatel', None)
        flash('Úspěšně odhlášen!', category='uspech')
        return redirect(url_for('auth.login'))
    else:
        flash('Uživatel není přihlášen', category='chyba')
        return redirect(url_for('auth.login'))
    #Hotovo pro Beta verzi :)

@auth.route('registrace', methods=['GET', 'POST']) #Povolení příjmu dat z frontendu
def sign_up(): #Definice funkce
    if request.method == 'POST': #Podmínka pro příjem dat
        e_mail = request.form.get('e_mail') #Proměnou z formuláře si uložíme do lokální proměnné
        heslo = request.form.get('heslo')
        hesloC = request.form.get('hesloC')
        if len(heslo) < 6: #Kontrola jestli heslo má více než 6 znaků
            flash('Uživatelské heslo musí mít alespoň 7 znaků!!!', category='chyba') #Vyskakovací zprávy
        elif heslo != hesloC: #Kontrola zhodnosti hesla
            flash('Hesla se neshodují, zkus to znovu!!!', category='chyba')
        else:
            flash('Registrace byla úspěšná!!!', category='uspech')
            uzivatel = prihlasovani.create_user_with_email_and_password(e_mail,heslo) #Vytvořnení uživatele v databázi 
            prihlasovani.send_email_verification(uzivatel['idToken']) #Odeslání kontrolního emailu
            return redirect(url_for('auth.login')) #Přesměrování na přihlašovací stránku
    return render_template("registrace.html") #Načtení šablony frontendu pro registraci

@auth.route('obnoveni', methods=['POST', 'GET'])
def obnoveni():
    if request.method == 'POST':
        e_mail = request.form.get('e_mail')
        try:
            prihlasovani.send_password_reset_email(e_mail)
            flash('Obnova hesla byla zaslána na zadný email!', category='uspech')
            return redirect(url_for('auth.login'))
        except:
            flash('Špatně zadaný email!', category='chyba')
    return render_template("obnova.html")
    #Hotovo pro Beta verzi :)

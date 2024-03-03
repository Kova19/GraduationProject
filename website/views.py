from flask import Blueprint, render_template, request, flash, redirect, session, Flask, url_for
from firebase_admin import firestore
from datetime import datetime

views = Blueprint('views', __name__)


@views.route('/')
def home():
    return redirect(url_for('auth.login'))

@views.route('/uzivatel', methods=['POST', 'GET'])
def uzivatel():
    cas = datetime.now() #Aktuální čas
    cas_ulozeni = cas.strftime("%d:%m:%Y:%H:%M:%S") #Naformátový čas
    if "uzivatel" in session: #Kontrola jestli je uživatel přihlášen
        uzivatel = session['uzivatel'] #Session je uložen do lokální proměnné
        vsechnyUkoly = '' #Vytvoření proměnné pro zobrazení úkolů
        db = firestore.client() #Configurace databáze
        ukoly = db.collection(uzivatel) #Vytažení dat z databáze
        dokumenty = ukoly.stream() #Zobrazení dat z databáze
        if request.method == 'POST':
            novy_ukol = request.form.get('novy_ukol')
            try: #Pokus o uložení dat do databáze
                flash('Úkol úspěšně uložen!', category='uspech')
                db.collection(uzivatel).document(cas_ulozeni).set({'Ukol': novy_ukol}) #Uložení dat do do databáze pod jméno uživatele a název souboru odpovídající datumu
            except:
                flash('Nezadal si žádný úkol!', category='chyba')
    else:
        return redirect(url_for('auth.login'))
    return render_template("domu.html", vsechnyUkoly=dokumenty)#Proměnná vechnyUkoly budou reprezentovat zobrazení v frontendu
    #Hotovo pro Beta verzi :)

@views.route('odstraneni/<dokument_id>', methods=['POST', 'GET'])
def odstraneni(dokument_id):
    if "uzivatel" in session:
        uzivatel = session['uzivatel']
        db = firestore.client()
        db.collection(uzivatel).document(dokument_id).delete()
    return redirect(url_for('views.uzivatel'))
    #Hotovo pro Beta verzi :)

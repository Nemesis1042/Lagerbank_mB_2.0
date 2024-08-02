# Standard-Bibliotheken
import os   # Für Dateioperationen
import sqlite3  # Für Datenbankzugriff
from datetime import datetime # Für Zeitstempel

# Externe Bibliotheken
import subprocess #
import numpy as np  #
import pandas as pd     # Für Datenverarbeitung und -analyse
import shutil   # Für Dateioperationen
from typing import List, Tuple, Callable    # Für Typenangaben
from collections import Counter

# Flask und zugehörige Erweiterungen
from flask import Flask, Response, render_template, request, redirect, url_for, flash, jsonify  # Für Webanwendungen
# Benutzerdefinierte Module
from database import Database, get_db_connection    # Für Datenbankzugriff

# Konfigurationen
from config import db_backup    # Für Backup-Konfiguration
from config import Zeltlager    # Für Lager-Konfiguration


# Initialisierung der Flask-App
app = Flask(__name__)
os.system('python DB_create.py')
app.config.from_object('config.Config')


# Funktionen
def get_users_from_db():
    print('get_users_from_db') # Debugging-Information
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Name FROM Teilnehmer ORDER BY T_ID")
    users = cursor.fetchall()
    conn.close()
    return [user['Name'] for user in users]

def get_products_from_db():
    print('get_products_from_db') # Debugging-Information
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Beschreibung FROM Produkt")
    products = cursor.fetchall()
    conn.close()
    return [product['Beschreibung'] for product in products]

def get_db():
    print('get_db') # Debugging-Information
    return sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'].split('///')[-1])

def submit_purchase(user, product_data):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    try:
        # Fetch user ID
        cursor.execute("SELECT T_ID FROM Teilnehmer WHERE TN_Barcode = ?", (user,))
        user_row = cursor.fetchone()
        if user_row is None:
            flash("Teilnehmer nicht gefunden!")
            return False
        T_ID = user_row['T_ID']
        
        # Fetch account balance
        cursor.execute("SELECT Kontostand FROM Konto WHERE T_ID = ?", (T_ID,))
        account_row = cursor.fetchone()
        if account_row is None:
            flash("Konto nicht gefunden!")
            return False
        Kontostand = round(account_row['Kontostand'], 2)
        
        for product, quantity in product_data.items():
            # Fetch product details
            cursor.execute("SELECT P_ID, Preis FROM Produkt WHERE P_Produktbarcode = ?", (product,))
            product_row = cursor.fetchone()
            if product_row is None:
                flash("Produkt nicht gefunden!")
                return False
            P_ID = product_row['P_ID']
            Preis = product_row['Preis']
            
            total_price = quantity * Preis
            if total_price > Kontostand:
                flash("Nicht genügend Guthaben!")
                return False
            
            new_Kontostand = round(Kontostand - total_price, 2)
            
            # Insert transaction
            cursor.execute("""
                INSERT INTO Transaktion (K_ID, P_ID, Typ, Menge, Datum)
                VALUES ((SELECT K_ID FROM Konto WHERE T_ID = ?), ?, ?, ?, ?)
            """, (T_ID, P_ID, 'Kauf', quantity, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
            
            # Update account balance and product sales
            cursor.execute("UPDATE Konto SET Kontostand = ? WHERE T_ID = ?", (new_Kontostand, T_ID))
            cursor.execute("UPDATE Produkt SET Anzahl_verkauft = Anzahl_verkauft + ? WHERE P_ID = ?", (quantity, P_ID))
            
            Kontostand = new_Kontostand  # Update Kontostand for the next iteration
        
        conn.commit()  # Commit all changes if everything is successful
        return True
    except Exception as e:
        conn.rollback()  # Rollback if an error occurs
        flash(f"Fehler beim Hinzufügen der Transaktion: {e}")
        return False
    finally:
        cursor.close()
        conn.close()

def fetch_users(db: Database) -> List[str]:
    print('fetch_users') # Debugging-Information
    users = [user[0] for user in db.execute_select("SELECT Name FROM Teilnehmer ORDER BY T_ID")]  # Ruft Benutzernamen aus der Datenbank ab
    return users

def fetch_products(db: Database):
    query = "SELECT Beschreibung FROM Produkt ORDER BY Preis"
    return [row[0] for row in db.execute_select(query)]

def fetch_transactions(db: Database, user_id: int) -> List[Tuple]:
    print('fetch_transactions') # Debugging-Information
    transactions = db.execute_select("SELECT * FROM Transaktion WHERE K_ID = ? ORDER BY Datum DESC", (user_id,))  # Ruft Transaktionen für einen bestimmten Benutzer ab
    return transactions

def kontostand_in_geld(kontostand):
    if kontostand:
        kontostand_value = kontostand
        zwischenstand = round(kontostand_value, 2)
    else:
        kontostand_value = 0
        zwischenstand = 0
    denominations = [20, 10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
    
    counts = {denom: 0 for denom in denominations}  # Korrektur: Initialisierung des Dictionaries
    
    for denom in denominations:
        count = int(zwischenstand) // denom
        counts[denom] += count  # Korrektur: Verwendung von counts[denom] anstelle von counts.append(count)
        zwischenstand -= count * denom
    return counts

def create_backup(source_file, backup_directory): 
    source_file = db_backup.source_file
    backup_directory = db_backup.backup_directory
    print("Erstelle Backup...") # Debugging-Information
    try:
        # Prüfen, ob die Quelldatei existiert
        if not os.path.isfile(source_file):
            raise FileNotFoundError(f"Die Quelldatei {source_file} wurde nicht gefunden.")

        # Sicherstellen, dass das Backup-Verzeichnis existiert
        if not os.path.exists(backup_directory):
            os.makedirs(backup_directory)

        # Name der Backup-Datei generieren
        base_name = os.path.basename(source_file)
        backup_file = os.path.join(backup_directory, "backup_" + base_name)

        # Datei kopieren
        shutil.copy2(source_file, backup_file)

        print(f"Backup erfolgreich erstellt: {backup_file}")
        
        return redirect(url_for("backup"))
    except Exception as e:
        print(f"Fehler beim Erstellen des Backups: {e}")
# Function to calculate the remaining balance until the end of the camp
def genug_geld_bis_ende_von_tag(teilnehmer_id, db):
    print("Berechne erwarteten Kontostand...")
    try:
        lager_name = Zeltlager.lager  # Example for the camp
        lager = db.execute("SELECT Zeltlager FROM Einstellungen WHERE Zeltlager = ?", (lager_name,)).fetchone()[0]
        
        # Convert date formats
        first_day = db.execute("SELECT first_day FROM Einstellungen WHERE Zeltlager = ?", (lager,)).fetchone()[0]
        end_datum = db.execute("SELECT last_day FROM Einstellungen WHERE Zeltlager = ?", (lager,)).fetchone()[0]
        referenz_datum = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Account balance at the reference date
        kontostand_referenz_datum = db.execute("SELECT Kontostand FROM Konto WHERE T_ID = ?", (teilnehmer_id,)).fetchone()[0]
        
        # Expenses between start date and reference date
        ausgaben = db.execute("SELECT SUM(Preis * Menge) FROM Transaktion JOIN Produkt ON Transaktion.P_ID = Produkt.P_ID WHERE K_ID = ? AND Datum BETWEEN ? AND ?", (teilnehmer_id, first_day, referenz_datum)).fetchone()[0]
        if ausgaben is None:
            ausgaben = 0
        
        # Days since the start of the camp
        tage_seit_anfang = (datetime.strptime(referenz_datum[:10], '%Y-%m-%d') - datetime.strptime(first_day, '%Y-%m-%d')).days
        
        # Days until the end of the camp
        tage_bis_ende = (datetime.strptime(end_datum[:10], '%Y-%m-%d') - datetime.strptime(referenz_datum[:10], '%Y-%m-%d')).days
        
        # Expenses per day
        ausgaben_pro_tag = ausgaben / tage_seit_anfang if tage_seit_anfang != 0 else 0
        
        # Account balance at the end of the camp
        erwarteter_kontostand_ende = kontostand_referenz_datum - (ausgaben_pro_tag * tage_bis_ende)      
        return erwarteter_kontostand_ende
    
    except Exception as e:
        print(f"Fehler bei der Berechnung des erwarteten Kontostands: {e}")
        return None

def aktualisere_endkontostand():
    print("Aktualisiere Endkontostand...")
    try:
        db = get_db_connection()
        # Get all participants
        teilnehmer = db.execute("SELECT T_ID FROM Teilnehmer").fetchall()
        
        for tn in teilnehmer:
            tn_id = tn[0]
            # Update end balance for each participant
            erwarteter_kontostand = genug_geld_bis_ende_von_tag(tn_id, db)
            erwarteter_kontostand = round(erwarteter_kontostand, 2) if erwarteter_kontostand is not None else None  
            if erwarteter_kontostand is not None:
                db.execute("UPDATE Konto SET Endkontostand = ? WHERE T_ID = ?", (erwarteter_kontostand, tn_id))
                print(f"Endkontostand für TN {tn_id} aktualisiert.")
            else:
                print(f"Fehler beim Aktualisieren des Endkontostands für TN {tn_id}")
        
        db.commit()
    
    except Exception as e:
        print(f"Fehler beim Aktualisieren des Endkontostands: {e}")
    finally:
        db.close()

def submit_borrow(user, item):
    print(f"Benutzer: {user}, Spielzeug: {item}")  # Debugging-Ausgabe
    try:
        db = get_db_connection()
        # Teilnehmer-ID und Spielzeug-ID aus der Anfrage holen
        TN_bacode = user
        spielzeug_name = item
        
        # Überprüfen, ob das Spielzeug bereits ausgeliehen wurde
        ausgeliehen = db.execute("SELECT Ausgeliehen FROM Spielzeug WHERE S_Barcode = ?", (spielzeug_name,)).fetchone()
        if ausgeliehen and ausgeliehen[0] == 1:
            flash(f"Das Spielzeug mit der ID {spielzeug_name} ist bereits ausgeliehen.", 'error')
            return False
        
        # Spielzeug-Ausleihe in die Datenbank eintragen
        spielzeug_id = db.execute("SELECT Spielzeug_ID FROM Spielzeug WHERE S_Barcode = ?", (spielzeug_name,)).fetchone()
        if not spielzeug_id:
            flash(f"Spielzeug mit Barcode {spielzeug_name} nicht gefunden.", 'error')  # Fehler als Flash-Nachricht
            return False
        teilnehmer_id = db.execute("SELECT T_ID FROM Teilnehmer WHERE TN_Barcode = ?", (TN_bacode,)).fetchone()
        if not teilnehmer_id:
            flash(f"Teilnehmer mit Barcode {TN_bacode} nicht gefunden.", 'error')  # Fehler als Flash-Nachricht
            return False
        
        db.execute("INSERT INTO Spielzeug_Ausleihe (Spielzeug_ID, T_ID, Ausleihdatum) VALUES (?, ?, CURRENT_DATE)", (spielzeug_id[0], teilnehmer_id[0]))
        db.execute("UPDATE Spielzeug SET Ausgeliehen = 1 WHERE Spielzeug_ID = ?", (spielzeug_id[0],))
        db.commit()
        print(f"Spielzeug mit der ID {spielzeug_name} wurde erfolgreich an Teilnehmer {teilnehmer_id[0]} ausgeliehen.")
        return True
    except Exception as e:
        flash(f"Fehler beim Ausleihen des Spielzeugs: {e}", 'error')  # Fehler als Flash-Nachricht
        return False

def barcode_exists(db: Database, barcode: str):
    query = "SELECT 1 FROM P_Barcode WHERE Barcode = ?"
    return bool(db.execute_select(query, (barcode,)))

def get_product_price(product_barcode):
    conn = get_db_connection()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT Preis FROM Produkt WHERE Beschreibung = ?", (product_barcode,))
    product_row = cursor.fetchone()
    conn.close()
    if product_row:
        return product_row['Preis']
    return 0

# Routen
@app.route('/', methods=['GET', 'POST'])
def index():
    print('index')
    with Database() as db:
        titel = db.execute_select("SELECT Zeltlagername FROM Einstellungen")
        if titel:
            titel = titel[0][0]
        else:
            titel = "Kein Titel gefunden"
    print(titel)
    return render_template('index.html', titel=titel)

@app.route('/db_create')
def db_create():
    print('db_create') # Debugging-Information
    os.system('python DB_create.py')
    return redirect(url_for('index'))

@app.route('/teilnehmer')
def teilnehmer():
    print('teilnehmer') # Debugging-Information
    return render_template('A_TN.html')

@app.route('/produkte')
def produkte():
    print('produkte') # Debugging-Information
    return render_template('A_Produkte.html')

@app.route('/statistik')
def statistik():
    print('statistik') # Debugging-Information
    return render_template('A_Statistik.html')

@app.route('/items')
def items():
    print('statistik') # Debugging-Information
    return render_template('A_spielzeug.html')

@app.route('/datenbankverwaltung')
def datenbankverwaltung():
    print('datenbankverwaltung') # Debugging-Information
    return render_template('A_DB.html')

@app.route('/admin')
def admin():
    print('admin') # Debugging-Information
    return render_template('admin.html')

@app.route('/update_product_dropdowns', methods=['GET'])
def update_product_dropdowns_route():
    print('update_product_dropdowns')
    db = Database()
    products = fetch_products(db)  # Ruft Produktbeschreibungen ab
    return jsonify({'products': products})

@app.route('/buy_check', methods=['GET', 'POST'])
def buy_check():
    if request.method == 'POST':
        user = request.form['user']
        products = request.form.getlist('products')
        
        # Aggregate product quantities
        product_data = dict(Counter(products))
        
        # Remove empty products
        product_data = {k: v for k, v in product_data.items() if k.strip()}

        # Calculate the total price
        total_price = sum(get_product_price(product) * quantity for product, quantity in product_data.items())
        total_price = "{:.2f}".format(total_price)

        success = submit_purchase(user, product_data)
        if success:
            flash(f"{user} hat {', '.join(product_data.keys())} für insgesamt {total_price} € erfolgreich gekauft", 'success')
            return redirect(url_for('success'))
        else:
            flash('Fehler beim Hinzufügen des Kaufs', 'danger')
            return redirect(url_for('add_buy'))
    else:
        username = request.args.get('username')
        products = request.args.getlist('products')

        # Aggregate product quantities
        product_data = dict(Counter(products))

        # Remove empty products
        product_data = {k: v for k, v in product_data.items() if k.strip()}

        # Calculate the total price
        if product_data:
            total_price = sum(get_product_price(product) * quantity for product, quantity in product_data.items())
        else:
            total_price = 3.40  # Default total price when no products are selected

        # Format total price to 2 decimal places
        total_price = "{:.2f}".format(total_price)

        return render_template('buy_check.html', username=username, product_data=product_data, gesammtpreis=total_price)

@app.route('/retry_purchase', methods=['GET', 'POST'])
def retry_purchase():
    print('retry_purchase')
    if request.method == 'POST':
        return redirect(url_for('add_buy'))

@app.route('/success')
def success():
    print("Purchase completed successfully!")
    return redirect(url_for("add_buy"))

@app.route('/success_borrow')
def success_borrow():
    print("Borrow completed successfully!")
    return redirect(url_for("index"))

@app.route('/borrow', methods=['GET', 'POST'])
def borrow():
    print('borrow')
    if request.method == 'POST':
        user = request.form['TN_Barcode']
        spielzeug = request.form['Spielzeug']
        print(spielzeug)
        
        # Redirect to the confirmation page
        return redirect(url_for('borrow_check', username=user, item=spielzeug))  # Ändern Sie 'items' zu 'item'  # Korrektur: 'items' zu 'spielzeug'
    
    conn = get_db_connection()
    IDs = conn.execute("SELECT T_ID FROM Teilnehmer").fetchall()
    conn.close()
    return render_template('borrow.html', IDs=IDs)

@app.route('/borrow_check', methods=['GET', 'POST'])
def borrow_check():
    if request.method == 'POST':
        user = request.form.get('user')
        item = request.form.get('item')
        if item is None:
            flash('Fehler: Item fehlt!', 'danger')
            return redirect(url_for('borrow'))
        success = submit_borrow(user, item)
        if success:
            print(f"{user} hat {item} erfolgreich ausgeliehen")
            return redirect(url_for('success_borrow'))
        else:
            flash('Fehler beim Hinzufügen der Ausleihe', 'danger')
            return redirect(url_for('borrow'))
    else:
        username = request.args.get('username')
        item = request.args.get('item')
        return render_template('borrow_check.html', username=username, item=item)

@app.route("/borrow_stats", methods=['GET', 'POST'])
def borrow_stats():
    conn = get_db_connection()
    spielzeuge = conn.execute('''
        SELECT 
            Spielzeug.Name, 
            Spielzeug.S_Barcode, 
            COUNT(Spielzeug_Ausleihe.Spielzeug_Ausleihe_ID) AS Ausleihen
        FROM 
            Spielzeug
        LEFT JOIN 
            Spielzeug_Ausleihe ON Spielzeug.Spielzeug_ID = Spielzeug_Ausleihe.Spielzeug_ID
        GROUP BY 
            Spielzeug.Spielzeug_ID
        ORDER BY 
            Ausleihen DESC
    ''').fetchall()
    conn.close()
    return render_template('borrow_stats.html', spielzeuge=spielzeuge)

@app.route('/watch')
def watch():
    print('watch') # Debugging-Information
    conn = get_db_connection()
    cursor = conn.cursor()
    aktualisere_endkontostand()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='Produkt';")
    if not cursor.fetchone():
        conn.close()
        return "Die Tabelle 'Produkt' existiert nicht in der Datenbank.", 404
    produkt_infos = cursor.execute("SELECT P_ID, Beschreibung, ROUND(Preis, 2) as Preis FROM Produkt").fetchall()
    produkt_summen = ", ".join([f"SUM(CASE WHEN Transaktion.P_ID = {pid} THEN Transaktion.Menge ELSE 0 END) AS '{desc} ({preis:.2f}€)'" for pid, desc, preis in produkt_infos])
    sql_query = f"""
        SELECT 
            Teilnehmer.Name,
            Konto.Einzahlung AS Einzahlung_€,
            printf('%04.2f', ROUND(Konto.Kontostand, 2)) AS Kontostand_€,
            printf('%04.2f', ROUND(Konto.Endkontostand, 2)) AS Endkontostand_€,
            {produkt_summen}
        FROM Teilnehmer 
        JOIN Konto ON Teilnehmer.T_ID = Konto.T_ID
        LEFT JOIN Transaktion ON Konto.K_ID = Transaktion.K_ID
        GROUP BY Teilnehmer.T_ID, Teilnehmer.Name, Konto.Einzahlung, ROUND(Konto.Kontostand, 2)
        ORDER BY Teilnehmer.T_ID;
    """
    result = cursor.execute(sql_query).fetchall()
    conn.close()
    df = pd.DataFrame(result, columns=[desc[0] for desc in cursor.description])
    return render_template('watch.html', tables=df.to_html(classes='data', header=True, index=False))

@app.route('/ausgeliehen')
def ausgeliehen():
    conn = get_db_connection()
    cursor = conn.cursor()

    query = '''
    SELECT 
        Spielzeug.Name,
        Teilnehmer.Name AS Teilnehmer
    FROM 
        Spielzeug
    LEFT JOIN 
        Spielzeug_Ausleihe ON Spielzeug.Spielzeug_ID = Spielzeug_Ausleihe.Spielzeug_ID AND Spielzeug_Ausleihe.Rückgabedatum IS NULL
    LEFT JOIN 
        Teilnehmer ON Spielzeug_Ausleihe.T_ID = Teilnehmer.T_ID
    '''
    cursor.execute(query)
    spielzeuge = cursor.fetchall()
    conn.close()
    
    return render_template('ausgeliehen.html', spielzeuge=spielzeuge)

@app.route('/login', methods=['GET', 'POST'])
def login():
    print('login') # Debugging-Information
    if request.method == 'POST':
        password = request.form['password']
        if password == '1':
            return redirect(url_for('admin'))
        else:
            print('Invalid password, try again.', 'danger')
    return render_template('login.html')

@app.route('/dblogin', methods=['GET', 'POST'])  # Hinzufügen des fehlenden Schrägs@
def dblogin():
    print('dblogin') # Debugging-Information
    if request.method == 'POST':
        passworddb = request.form['passworddb']
        if passworddb == 'FwvdDB':
            return redirect(url_for('datenbankverwaltung'))
        else:
            print('Invalid password, try again.', 'danger')
    return render_template('loginform.html')

@app.route('/add_buy', methods=['GET', 'POST'])
def add_buy():
    print('add_buy')
    if request.method == 'POST':
        user = request.form['TN_Barcode']
        products = [request.form[f'P_Barcode{i}'] for i in range(1, 8) if f'P_Barcode{i}' in request.form]
        print(products)
        
        # Redirect to the confirmation page
        return redirect(url_for('buy_check', username=user, products=products, quantity=1))
    
    conn = get_db_connection()
    IDs = conn.execute("SELECT T_ID FROM Teilnehmer").fetchall()
    conn.close()
    return render_template('add_buy.html', IDs=IDs)

@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    print('add_user') # Debugging-Information
    if request.method == 'POST':
        user = request.form['user']
        # Korrektur: Überprüfen, ob 'TN_B' im Formular vorhanden ist
        TN_Barocde = request.form.get('TN_B', None)  # Verwenden von get() um Fehler zu vermeiden
        if TN_Barocde is None:
            flash('Fehler: TN_B Barcode fehlt!', 'danger')
            return redirect(url_for('add_user'))  # Umleitung bei fehlendem Barcode
        amount = float(request.form['amount'])
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT Name FROM Teilnehmer WHERE Name = ?", (user,))
        if cur.fetchone():
            flash('Benutzer existiert bereits!', 'danger')
        else:
            cur.execute("INSERT INTO Teilnehmer (Name, TN_Barcode) VALUES (?,?)", (user,TN_Barocde,))
            t_id = cur.execute("SELECT T_ID FROM Teilnehmer WHERE Name = ?", (user,)).fetchone()[0]
            cur.execute("INSERT INTO Konto (Einzahlung, Kontostand, Eröffnungsdatum, T_ID) VALUES (?, ?, ?, ?)",
                        (amount, amount, datetime.now().strftime("%d.%m.%Y"), t_id))
            cur.execute("INSERT INTO Transaktion (K_ID, P_ID, Typ, Menge, Datum) VALUES (?, ?, ?, ?, ?)", (t_id, 0, 'Einzahlung', amount, datetime.now().strftime("%d.%m.%Y %H:%M:%S")))
            conn.commit()
            print('Benutzer erfolgreich hinzugefügt.', 'success')
        conn.close()
        return redirect(url_for('teilnehmer'))
    return render_template('add_user.html')

@app.route('/add_fund', methods=['GET', 'POST'])
def add_fund():
    print('add_fund') # Debugging-Information
    if request.method == 'POST':
        user = request.form['user']
        amount = float(request.form['amount'])
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT Name FROM Teilnehmer WHERE Name = ?", (user,))
        if not cur.fetchone():
            flash('Benutzer nicht gefunden!', 'danger')
        else:
            user_balance = cur.execute("SELECT Kontostand FROM Konto JOIN Teilnehmer ON Konto.T_ID = Teilnehmer.T_ID WHERE Teilnehmer.Name = ?", (user,)).fetchone()
            user_einzahlung = cur.execute("SELECT Einzahlung FROM Konto JOIN Teilnehmer ON Konto.T_ID = Teilnehmer.T_ID WHERE Teilnehmer.Name = ?", (user,)).fetchone()
            if user_balance:
                new_balance = user_balance['Kontostand'] + amount
                cur.execute("UPDATE Konto SET Kontostand = ? WHERE T_ID = (SELECT T_ID FROM Teilnehmer WHERE Name = ?)", (new_balance, user))
                cur.execute("INSERT INTO Transaktion (K_ID, P_ID, Typ, Menge, Datum) VALUES ((SELECT T_ID FROM Teilnehmer WHERE Name = ?), 0, 'Einzahlung', ?, ?)", (user, amount, datetime.now().strftime("%d.%m.%Y %H:%M:%S")))
                new_einzahlung = user_einzahlung['Einzahlung'] + amount
                cur.execute("UPDATE Konto SET Einzahlung = ? WHERE T_ID = (SELECT T_ID FROM Teilnehmer WHERE Name = ?)", (new_einzahlung, user)) # Update the deposit
                conn.commit()
                print(f'{amount} € erfolgreich hinzugefügt.', 'success')
            else:
                flash('Benutzer hat kein Kontoguthaben!', 'danger')
        conn.close()
        return redirect(url_for('admin'))
    else:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT Name FROM Teilnehmer")
        users = [row[0] for row in cur.fetchall()]
        conn.close()
        return render_template('add_fund.html', users=users)

@app.route('/add_spielzeug', methods=['GET', 'POST'])
def add_spielzeug():
    if request.method == 'POST':
        spielzeug_name = request.form['name']
        spielzeug_barcode = request.form['barcode']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Spielzeug WHERE S_Barcode = ?", (spielzeug_barcode,))
        if cur.fetchone():
            print('Spielzeug existiert bereits!', 'danger')
        else:
            cur.execute("INSERT INTO Spielzeug (Name, S_Barcode) VALUES (?, ?)", (spielzeug_name, spielzeug_barcode))
            conn.commit()
            print('Spielzeug erfolgreich hinzugefügt.', 'success')
        conn.close()
        return redirect(url_for('items'))
    else:
        return render_template('add_spielzeug.html')

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    print('add_product') # Debugging-Information
    if request.method == 'POST':
        product = request.form['product']
        P_barcode = request.form['P_barcode']
        price = float(request.form['price'])
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT Beschreibung FROM Produkt WHERE Beschreibung = ?", (product,))
        if cur.fetchone():
            flash('Produkt existiert bereits!', 'danger')
        else:
            cur.execute("INSERT INTO Produkt (Beschreibung, P_Produktbarcode, Preis, Anzahl_verkauft) VALUES (?, ?,?, 0)", (product, P_barcode, price))
            conn.commit()
            print('Produkt erfolgreich hinzugefügt.', 'success')
        conn.close()
        return redirect(url_for('admin'))
    return render_template('add_product.html')

@app.route('/edit_user', methods=['GET', 'POST'])
def edit_user():
    print('edit_user')  # Debugging-Information
    if request.method == 'POST':
        selected_user = request.form.get('selected_user')
        action = request.form.get('action')
        conn = get_db_connection()
        cur = conn.cursor()

        if action == 'update':
            new_name = request.form.get('new_name')
            if not selected_user or not new_name:
                print('Bitte füllen Sie alle Felder aus.', 'danger')
                return redirect(url_for('edit_user'))
            try:
                cur.execute("UPDATE Teilnehmer SET Name = ? WHERE Name = ?", (new_name, selected_user))
                conn.commit()
                print('Benutzername erfolgreich aktualisiert.', 'success')
            except Exception as e:
                flash(f'Fehler beim Aktualisieren des Benutzernamens: {e}', 'danger')

        elif action == 'update_b':
            new_barcode = request.form.get('new_barcode')
            if not selected_user or not new_barcode:
                print('Bitte füllen Sie alle Felder aus.', 'danger')
                return redirect(url_for('edit_user'))
            try:
                cur.execute("UPDATE Teilnehmer SET TN_Barcode = ? WHERE Name = ?", (new_barcode, selected_user))
                conn.commit()
                print('Barcode erfolgreich aktualisiert.', 'success')
            except Exception as e:
                flash(f'Fehler beim Aktualisieren des Barcodes: {e}', 'danger')

        elif action == 'delete':
            if not selected_user:
                print('Bitte wählen Sie einen Benutzer aus.', 'danger')
                return redirect(url_for('edit_user'))
            try:
                cur.execute("DELETE FROM Konto WHERE T_ID = (SELECT T_ID FROM Teilnehmer WHERE Name = ?)", (selected_user,))
                cur.execute("DELETE FROM Teilnehmer WHERE Name = ?", (selected_user,))
                conn.commit()
                flash('Benutzer erfolgreich gelöscht.', 'success')
            except Exception as e:
                flash(f'Fehler beim Löschen des Benutzers: {e}', 'danger')

        conn.close()
        return redirect(url_for('edit_user'))
    else:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT Name FROM Teilnehmer")
        users = [row[0] for row in cur.fetchall()]
        conn.close()
        return render_template('edit_user.html', users=users)

@app.route('/edit_spielzeug', methods=['GET', 'POST'])
def edit_spielzeug():
    if request.method == 'POST':
        selected_spielzeug = request.form.get('selected_spielzeug')
        new_name = request.form.get('new_name')
        new_barcode = request.form.get('new_barcode')
        action = request.form.get('action')

        if action == 'update':
            if not selected_spielzeug or not new_name or not new_barcode:
                flash('Bitte füllen Sie alle Felder aus.', 'danger')
                return redirect(url_for('edit_spielzeug'))
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("UPDATE Spielzeug SET Name = ?, S_Barcode = ? WHERE Name = ?", (new_name, new_barcode, selected_spielzeug))
                conn.commit()
                print('Spielzeug erfolgreich bearbeitet.')
            except Exception as e:
                flash(f'Fehler beim Bearbeiten des Spielzeugs: {e}', 'danger')
            finally:
                conn.close()
        
        elif action == 'delete':
            if not selected_spielzeug:
                flash('Bitte wählen Sie ein Spielzeug aus.', 'danger')
                return redirect(url_for('edit_spielzeug'))
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("DELETE FROM Spielzeug WHERE Name = ?", (selected_spielzeug,))
                conn.commit()
                print('Spielzeug erfolgreich gelöscht.')
            except Exception as e:
                flash(f'Fehler beim Löschen des Spielzeugs: {e}', 'danger')
            finally:
                conn.close()

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT Name FROM Spielzeug")
        spielzeuge = cur.fetchall()
    except Exception as e:
        flash(f'Fehler beim Abrufen der Spielzeuge: {e}', 'danger')
        spielzeuge = []
    finally:
        conn.close()

    return render_template('edit_spielzeug.html', spielzeuge=spielzeuge)

@app.route('/edit_product_prices', methods=['GET', 'POST'])
def edit_product_prices():
    print('edit_product_prices') # Debugging-Information
    if request.method == 'POST':
        selected_product = request.form.get('selected_product')
        action = request.form.get('action')
        
        
        if action == 'update': # Aktualisieren des Produktpreises
            new_price_str = request.form.get('new_price')
            if new_price_str:
                try:
                    new_price = float(new_price_str)
                except ValueError:
                    print('Bitte geben Sie einen gültigen Preis ein.', 'danger')
                    return redirect(url_for('edit_product_prices'))
            else:
                new_price = None
            if not selected_product: 
                flash('Bitte wählen Sie ein Produkt aus.', 'danger')
                return redirect(url_for('edit_product_prices'))
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                if new_price is not None:
                    cur.execute("UPDATE Produkt SET Preis = ? WHERE Beschreibung = ?", (new_price, selected_product))
                    conn.commit()
                    print('Produktpreis erfolgreich aktualisiert.', 'success')
            except Exception as e:
                print(f'Fehler: {e}', 'danger')
            finally:
                conn.close()
                
        elif action == 'update_barcode': # Aktualisieren des Barcodes
            new_barcode = request.form.get('new_barcode')
            if not new_barcode:
                print('Bitte geben Sie einen neuen Barcode ein.', 'danger')
                return redirect(url_for('edit_product_prices'))
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("UPDATE Produkt SET P_Produktbarcode = ? WHERE Beschreibung = ?", (new_barcode, selected_product))
                conn.commit()
                print('Barcode erfolgreich aktualisiert.', 'success')
            except Exception as e:
                print(f'Fehler: {e}', 'danger')
            finally:
                conn.close()
                
        elif action == 'delete': # Löschen des Produkts
            if not selected_product:
                print('Bitte wählen Sie ein Produkt aus.', 'danger')
                return redirect(url_for('edit_product_prices'))
            try:
                conn = get_db_connection()
                cur = conn.cursor()
                cur.execute("UPDATE Produkt SET Preis = 0.00 WHERE Beschreibung = ?", (selected_product,))
                conn.commit()
                cur.execute("DELETE FROM Produkt WHERE Beschreibung = ?", (selected_product,))
                conn.commit()
                print('Produkt erfolgreich gelöscht.', 'success')
            except Exception as e:
                print(f'Fehler: {e}', 'danger')
            finally:
                conn.close()
        else:
            print('Ungültige Aktion.', 'danger')
            return redirect(url_for('edit_product_prices'))
        return redirect(url_for('admin'))
    else:
        products = get_products_from_db()
        return render_template('edit_product_prices.html', products=products)

@app.route('/withdraw_fund', methods=['GET', 'POST'])
def withdraw_fund():
    print('withdraw_fund') # Debugging-Information
    if request.method == 'POST':
        user = request.form['user']
        amount = float(request.form['amount'])
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT Name FROM Teilnehmer WHERE TN_Barcode = ?", (user,))
        if not cur.fetchone():
            flash('Benutzer nicht gefunden!', 'danger')
        else:
            current_balance = cur.execute("SELECT Kontostand FROM Konto JOIN Teilnehmer ON Konto.T_ID = Teilnehmer.T_ID WHERE Teilnehmer.TN_Barcode = ?", (user,)).fetchone()
            current_balance = current_balance['Kontostand'] if current_balance else 0
            user_balance = cur.execute("SELECT Kontostand FROM Konto JOIN Teilnehmer ON Konto.T_ID = Teilnehmer.T_ID WHERE Teilnehmer.TN_Barcode = ?", (user,)).fetchone()
            if user_balance:
                if amount > user_balance['Kontostand']:
                    flash('Unzureichendes Guthaben!', 'danger')
                else:
                    new_balance = user_balance['Kontostand'] - amount
                    cur.execute("UPDATE Konto SET Kontostand = ? WHERE T_ID = (SELECT T_ID FROM Teilnehmer WHERE TN_Barcode = ?)", (new_balance, user))
                    cur.execute("INSERT INTO Transaktion (K_ID, P_ID, Typ, Menge, Datum) VALUES ((SELECT T_ID FROM Teilnehmer WHERE Name = ?), 0, 'Auszahlung', ?, ?)", (user, amount, datetime.now().strftime("%d.%m.%Y %H:%M:%S")))
                    conn.commit()
                    print(f'{amount} € erfolgreich abgehoben.', 'success')
            else:
                flash('Benutzer hat kein Kontoguthaben!', 'danger')
        conn.close()
        return redirect(url_for('teilnehmer'))
    else:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT Name FROM Teilnehmer")
        users = [row[0] for row in cur.fetchall()]
        conn.close()
        return render_template('withdraw_fund.html', users=users)

@app.route('/return_spielzeug', methods=['POST', 'GET'])
def return_spielzeug():
    print('return_spielzeug') # Debugging-Information
    if request.method == 'POST':
        TN_Barcode = request.form['TN_Barcode']
        Spielzeug = request.form['Spielzeug']
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM Spielzeug WHERE S_Barcode = ?", (Spielzeug,))
        spielzeug = cur.fetchone()
        if not spielzeug:
            print('Spielzeug nicht gefunden!', 'danger')
        else:
            cur.execute("SELECT * FROM Spielzeug_Ausleihe WHERE Spielzeug_ID = ? AND Rückgabedatum IS NULL", (spielzeug[0],))
            ausleihe = cur.fetchone()
            if not ausleihe:
                print('Spielzeug ist nicht ausgeliehen.', 'danger')
            else:
                cur.execute("UPDATE Spielzeug_Ausleihe SET Rückgabedatum = ? WHERE Spielzeug_Ausleihe_ID = ?", (datetime.now().strftime("%d.%m.%Y"), ausleihe[0]))
                cur.execute("UPDATE Spielzeug SET Ausgeliehen = 0 WHERE Spielzeug_ID = ?", (spielzeug[0],))
                conn.commit()
                print('Spielzeug erfolgreich zurückgegeben.', 'success')
        conn.close()
        return redirect(url_for('index'))
    else:
        return render_template ("back.html")

@app.route('/checkout_tn')
def checkout_tn():
    print('checkout_tn') # Debugging-Information
    with Database() as db:
        users = db.execute_select("SELECT Name FROM Teilnehmer ORDER BY Name")
    return render_template('TN-Abfrage.html', users=[user[0] for user in users])

@app.route('/checkout', methods=['POST'])
def checkout():
    print('checkout') # Debugging-Information
    benutzer_id = request.form['user']
    if not benutzer_id:
        print("Bitte wählen Sie einen Teilnehmer aus.", 'danger')
        return redirect(url_for('index'))
    
    with Database() as db:
        users = db.execute_select("SELECT Name FROM Teilnehmer ORDER BY Name")
        if benutzer_id not in [user[0] for user in users]:
            print("Der ausgewählte Teilnehmer existiert nicht.", 'danger')
            alert = "Der ausgewählte Teilnehmer existiert nicht."
            return redirect(url_for('index', alert=alert))
        
        kontostand = db.execute_select("SELECT Kontostand FROM Konto WHERE T_ID = (SELECT T_ID FROM Teilnehmer WHERE Name = ?)", (benutzer_id,))
        kontostand = float(kontostand[0][0])
        kontostand = round(kontostand, 2)
        
        geldwerte = kontostand_in_geld(kontostand)
        if geldwerte is None:
            geldwerte = [0] * 11
        
        # Calculate the breakdown of banknotes and coins
        denominations = [20, 10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
        counts = {denom: 0 for denom in denominations}
        zwischenstand = kontostand
        
        for denom in denominations:
            count = int(zwischenstand // denom)
            counts[denom] = count
            zwischenstand -= count * denom
            zwischenstand = round(zwischenstand, 10)
        
        return render_template('checkout_c.html', benutzer_id=benutzer_id, kontostand=kontostand if kontostand else 0, geldwerte=geldwerte, counts=counts)

@app.route('/confirm_checkout', methods=['POST'])
def confirm_checkout():
    print('confirm_checkout') # Debugging-Information
    benutzer_id = request.form['user']
    with Database() as db:
        db.execute_update("UPDATE Konto SET Kontostand = 0 WHERE T_ID = (SELECT T_ID FROM Teilnehmer WHERE Name = ?)", (benutzer_id,))
        db.execute_update("UPDATE Teilnehmer SET Checkout = 1 WHERE Name = ?", (benutzer_id,))
    print("Checkout abgeschlossen.", 'success')
    return redirect(url_for('index'))

@app.route('/kaufstatistik')
def create_kaufstatistik_tab():
    print('kaufstatistik') # Debugging-Information
    try:
        with Database() as db:
            sql_query = '''
                        SELECT Produkt.Beschreibung, SUM(Transaktion.Menge) AS Anzahl_verkauft
                        FROM Produkt
                        JOIN Transaktion ON Produkt.P_ID = Transaktion.P_ID
                        GROUP BY Produkt.Beschreibung
                        ORDER BY Anzahl_verkauft DESC;
                        '''
            result = db.execute_select(sql_query)
            df = pd.DataFrame(result, columns=[desc[0] for desc in db.cursor.description])
            data = df.to_dict(orient='records')
        return render_template('kaufstatistik.html', data=data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/geld_aufteilen')
def geld_aufteilen():
    print('geld_aufteilen') # Debugging-Information
    conn = get_db_connection()
    kontos = conn.execute("SELECT K_ID, Kontostand FROM Konto").fetchall()
    conn.close()

    denominations = [20, 10, 5, 2, 1, 0.5, 0.2, 0.1, 0.05, 0.02, 0.01]
    counts = {denom: 0 for denom in denominations}

    for konto in kontos:
        kontostand = konto['Kontostand']
        zwischenstand = kontostand  # Keine Rundung auf 3 Dezimalstellen
        for denom in denominations:
            count = int(zwischenstand // denom)
            counts[denom] += count
            zwischenstand -= count * denom
            # Optional: Rundung hier, falls gewünscht, aber mit größerer Präzision
            zwischenstand = round(zwischenstand, 10)  # Erhöhte Präzision

    sume = sum(denom * count for denom, count in counts.items())
    gesamt_kontostand = sum(konto['Kontostand'] for konto in kontos)
    results = {"counts": counts, "sume": sume, "gesamt_kontostand": gesamt_kontostand}
   
    print(sume)
    print(gesamt_kontostand)
    print(results)
    return render_template('results.html', results=results)

@app.route('/backup', methods=['GET', 'POST'])
def backup_database():
    print('backup_database')  # Debugging-Information
    
    # Set default backup directory
    backup_directory = app.config.get('BACKUP_DIRECTORY', '"/home/arkatosh/Documents/CVJM/Bula/Lagerbank"')

    if request.method == 'POST':
        # Get new value from the form
        new_backup_directory = request.form['backup_directory']

        # Update configuration value
        app.config['BACKUP_DIRECTORY'] = new_backup_directory

        source_file = db_backup.source_file
        
        # Perform the backup with the new directory
        create_backup(source_file, new_backup_directory)

        return redirect(url_for('backup_database'))
    
    return render_template('backup.html', backup_directory=backup_directory)

@app.route('/delete_database', methods=['GET', 'POST'])
def delete_database():
    print('delete_database') # Debugging-Information
    if request.method == 'POST':
        password = request.form['password']
        if password == 'IchWillDieDatenbankLöschen':
            try:
                conn = get_db_connection()
                with open('database_backup.sql', 'w') as f:
                    for line in conn.iterdump():
                        f.write('%s\n' % line)
                print('Datenbank erfolgreich gesichert.', 'success')
                conn.execute("DROP TABLE IF EXISTS Teilnehmer")
                conn.execute("DROP TABLE IF EXISTS Konto")
                conn.execute("DROP TABLE IF EXISTS Produkt")
                conn.commit()
                print('Datenbank erfolgreich gelöscht.', 'success')
            except Exception as e:
                print(f'Fehler beim Löschen der Datenbank: {e}', 'danger')
            return redirect(url_for('delete_database'))
        else:
            print('Ungültiges Passwort!', 'danger')
    return render_template('delete_database.html')

@app.route('/settings', methods=['GET', 'POST'])
def settings():
    print('settings') # Debugging-Information  
    conn = get_db_connection()
    
    if request.method == 'POST':
        try:
            # Get dates and name from form
            first_day = request.form['formatted_first_day']
            last_day = request.form['formatted_last_day']
            lagername = request.form['lagername']
            
            # Validate and convert dates
            if first_day and last_day and lagername:
                # Convert to '%Y-%m-%d' format for database update
                first_day_db_format = datetime.strptime(first_day, '%d-%m-%Y').strftime('%Y-%m-%d')
                last_day_db_format = datetime.strptime(last_day, '%d-%m-%Y').strftime('%Y-%m-%d')
                
                # Update database
                conn.execute("UPDATE Einstellungen SET first_day = ?, last_day = ?, Zeltlagername = ? WHERE Zeltlager = ?", 
                             (first_day_db_format, last_day_db_format, lagername, Zeltlager.lager))
                conn.commit()
                
                print("Erfolg: Einstellungen erfolgreich aktualisiert.")
                return redirect(url_for('settings'))  # Redirect to GET /settings after POST
            else:
                print("Fehler: Eingabe für Erster Tag, Letzter Tag oder Lagername ist leer.")
                return redirect(url_for('settings'))
            
        except Exception as e:
            print(f"Fehler beim Aktualisieren der Einstellungen: {e}")
            return redirect(url_for('settings'))
    
    # Handle GET request to populate form fields
    first_day_row = conn.execute("SELECT first_day FROM Einstellungen WHERE Zeltlager = ?", (Zeltlager.lager,)).fetchone()
    last_day_row = conn.execute("SELECT last_day FROM Einstellungen WHERE Zeltlager = ?", (Zeltlager.lager,)).fetchone()
    lagername_row = conn.execute("SELECT Zeltlagername FROM Einstellungen WHERE Zeltlager = ?", (Zeltlager.lager,)).fetchone()
    
    conn.close()
    
    first_day = datetime.strptime(first_day_row['first_day'], '%Y-%m-%d').strftime('%d-%m-%Y') if first_day_row else ''
    last_day = datetime.strptime(last_day_row['last_day'], '%Y-%m-%d').strftime('%d-%m-%Y') if last_day_row else ''
    lagername = lagername_row['Zeltlagername'] if lagername_row else ''
    
    lager_dauer = (datetime.strptime(last_day, '%d-%m-%Y') - datetime.strptime(first_day, '%d-%m-%Y')).days
    
    heute = datetime.now().strftime('%d-%m-%Y')
    
    # Render settings page with form fields
    
    return render_template('settings.html', first_day=first_day, lager_dauer=lager_dauer, last_day=last_day, today=heute, lagername=lagername)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
#!/usr/bin/python3
import sqlite3
import os

datenbankname = "Lagerbank2024.db"


def create_database(datenbankname):
    # Ensure the directory exists
    directory = os.path.dirname(datenbankname)
    if not os.path.exists(directory):
        print(f"Creating directory: {directory}")
        os.makedirs(directory)
    
    print(f"Database path: {datenbankname}")
    
    # Connect to the database (create if it does not exist)
    try:
        connection = sqlite3.connect(datenbankname)
        cursor = connection.cursor()
        # Create tables or do other database setup here
        cursor.execute('''CREATE TABLE IF NOT EXISTS Teilnehmer (
        T_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        Name VARCHAR(50),
        TN_Barcode VARCHAR(50),
        Checkout BOOLEAN DEFAULT 0
        );
        ''')
        cursor.connection.commit()
    except sqlite3.OperationalError as e:
        print(f"Error: {e}")
        raise

    # Verbindung zur Datenbank herstellen
    connection = sqlite3.connect(datenbankname)
    cursor = connection.cursor()

    # Tabelle "Produkte" erstellen
    cursor.execute('''CREATE TABLE IF NOT EXISTS Produkt (
        P_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Beschreibung VARCHAR(100),
        P_Produktbarcode VARCHAR(50),
        Preis DECIMAL(10, 2),
        Anzahl_verkauft INT
        
    );    
    ''')
    cursor.connection.commit()
    
    # Tabelle "Spielzeug" erstellen
    cursor.execute('''CREATE TABLE IF NOT EXISTS Spielzeug (
        Spielzeug_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name VARCHAR(100),
        S_Barcode VARCHAR(100),
        "Ausgeliehen" BOOLEAN DEFAULT 0
    );
    ''')
    cursor.connection.commit()
    
    # Tabelle "Spielzeug_Ausleihe" erstellen 
    cursor.execute('''CREATE TABLE IF NOT EXISTS Spielzeug_Ausleihe (
        Spielzeug_Ausleihe_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Spielzeug_ID INT,
        T_ID INT,
        Ausleihdatum DATE,
        Rückgabedatum DATE,
        FOREIGN KEY (Spielzeug_ID) REFERENCES Spielzeug(Spielzeug_ID),
        FOREIGN KEY (T_ID) REFERENCES Teilnehmer(T_ID)
    );
    ''')
    cursor.connection.commit()
    
    # Tabelle "Teilnehmer" erstellen
    cursor.execute('''CREATE TABLE IF NOT EXISTS Teilnehmer (
        T_ID INTEGER PRIMARY KEY AUTOINCREMENT, 
        Name VARCHAR(50),
        TN_Barcode VARCHAR(50),
        Checkout BOOLEAN DEFAULT 0
    );
    
    ''')
    cursor.connection.commit()
    # Tabelle "Konto" erstellen
    cursor.execute('''CREATE TABLE IF NOT EXISTS Konto (
        K_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Einzahlung DECIMAL(10, 2),
        Kontostand DECIMAL(10, 2),
        Endkontostand DECIMAL(10, 2),
        Eröffnungsdatum DATE,
        T_ID INT,
        FOREIGN KEY (T_ID) REFERENCES Teilnehmer(T_ID)
    );
    
    ''')
    cursor.connection.commit()
    # Tabelle "Transaktion" erstellen
    cursor.execute('''CREATE TABLE IF NOT EXISTS Transaktion (
        TRANS_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        K_ID INT,
        P_ID INT,  -- Spalte für den Fremdschlüssel zur Produkt-Tabelle
        Typ VARCHAR(50),
        Menge INT,
        Datum DATE,
        FOREIGN KEY (K_ID) REFERENCES Konto(K_ID),
        FOREIGN KEY (P_ID) REFERENCES Produkt(P_ID)  -- Fremdschlüsselbeziehung zu Produkt
    );
    ''')
    cursor.connection.commit()
    
    # Tabelle "Einstellungen" erstellen
    cursor.execute('''CREATE TABLE IF NOT EXISTS Einstellungen (
        first_day DATE,
        last_day DATE,
        Zeltlager INT,
        Zeltlagername VARCHAR(50)
    );''')
    cursor.connection.commit()

    # Daten in die Tabelle "Einstellungen" einfügen
    cursor.execute('''INSERT INTO Einstellungen (first_day, last_day, Zeltlager, Zeltlagername) 
                      SELECT '2024-01-01', '2024-12-31', '2024', 'BuLa'
                      WHERE NOT EXISTS (SELECT 1 FROM Einstellungen)''')
    cursor.connection.commit()
    print("Einstellungen wurden erfolgreich erstellt!")
    print("2024")
    
    cursor.execute('''INSERT INTO Produkt (Beschreibung,P_Produktbarcode, Preis, Anzahl_verkauft) 
                      SELECT 'Medium','Medium','0.40', '0' 
                      WHERE NOT EXISTS (SELECT 1 FROM Produkt WHERE Beschreibung = 'Medium')''')
    cursor.connection.commit()
    print("Medium")
    
    cursor.execute('''INSERT INTO Produkt (Beschreibung,P_Produktbarcode, Preis, Anzahl_verkauft) 
                      SELECT 'Still','Still', '0.40', '0' 
                      WHERE NOT EXISTS (SELECT 1 FROM Produkt WHERE Beschreibung = 'Still')''')
    cursor.connection.commit()
    print("Still")
    
    cursor.execute('''INSERT INTO Produkt (Beschreibung,P_Produktbarcode, Preis, Anzahl_verkauft) 
                      SELECT 'Cola-Mix','Cola-Mix','0.60', '0' 
                      WHERE NOT EXISTS (SELECT 1 FROM Produkt WHERE Beschreibung = 'Cola-Mix')''')
    cursor.connection.commit()
    print("Cola-Mix")
    
    cursor.execute('''INSERT INTO Produkt (Beschreibung,P_Produktbarcode, Preis, Anzahl_verkauft) 
                      SELECT 'Rote-Schorle', 'Rote-Schorle','0.65', '0' 
                      WHERE NOT EXISTS (SELECT 1 FROM Produkt WHERE Beschreibung = 'Rote-Schorle')''')
    cursor.connection.commit()
    print("Rote-Schorle")
    
    cursor.execute('''INSERT INTO Produkt (Beschreibung,P_Produktbarcode, Preis, Anzahl_verkauft) 
                      SELECT 'Apfelschorle','Apfelschorle','0.65', '0' 
                      WHERE NOT EXISTS (SELECT 1 FROM Produkt WHERE Beschreibung = 'Apfelschorle')''')
    cursor.connection.commit()
    print("Apfelschorle")
    
    cursor.execute('''INSERT INTO Produkt (Beschreibung,P_Produktbarcode, Preis, Anzahl_verkauft) 
                      SELECT 'ISO-Grape','ISO-Grape', '0.65', '0' 
                      WHERE NOT EXISTS (SELECT 1 FROM Produkt WHERE Beschreibung = 'ISO-Grape')''')
    cursor.connection.commit()
    print("ISO-Grape")
    
    print("Produkte wurden erfolgreich erstellt!")
    # Verbindung schließen
    connection.close()
    print(f'Datenbank "{datenbankname}" wurde erfolgreich erstellt!')


if __name__ == "__main__":
    # Determine the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    datenbankname = os.path.join(script_dir, "Lagerbank2024.db")
    
    create_database(datenbankname)
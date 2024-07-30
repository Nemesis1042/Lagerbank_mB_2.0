#!/bin/bash

# Define the directory where the HTML files will be created
html_directory="/home/lager/Lagerbank/templates"

# Define the file names and their respective contents
declare -A files

files["A_DB.html"]='
<!DOCTYPE html>
<html lang="de">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>

<body>
    <header>
        <h1 class="topic">Admin Panel</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="/watch">Übersicht</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <div class="admin-content">
        <h2>Datenbankverwaltung</h2>
        <a href="/db_create" class="admin-link">Datenbank erstellen</a>
        <a href="/backup" class="admin-link">Datenbank sichern</a>
        <a href="/delete_database" class="admin-link">Datenbank löschen</a>
    </div>
</body>

</html>'

files["A_Produkte.html"]='<!DOCTYPE html>
<html lang="de">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>

<body>
    <header>
        <h1 class="topic">Admin Panel</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="/watch">Übersicht</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <div class="admin-content">
        <h2>Produkteinstellungen</h2>
        <a href="/add_product" class="admin-link">Produkt hinzufügen</a>
        <a href="/edit_product_prices" class="admin-link">Produkt bearbeiten</a>
    </div>
</body>

</html>'

files["A_Statistik.html"]='<!DOCTYPE html>
<html lang="de">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>

<body>
    <header>
        <h1 class="topic">Admin Panel</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="/watch">Übersicht</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <div class="admin-content">
        <h2>Statisiken</h2>
        <a href="/kaufstatistik" class="admin-link">Kaufstatistik</a>
        <a href="/geld_aufteilen" class="admin-link">Geldaufteilung</a>
        <a href="/watch" class="admin-link">Übersicht</a>
    </div>
</body>

</html>'

files["A_TN.html"]='<!DOCTYPE html>
<html lang="de">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>

<body>
    <header>
        <h1 class="topic">Admin Panel</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="/watch">Übersicht</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <div class="admin-content">
        <h2>Teilnehmerverwaltung</h2>
        <a href="/add_user" class="admin-link">Teilnehmer hinzufügen</a>
        <a href="/edit_user" class="admin-link">Teilnehmer bearbeiten</a>
        <a href="/add_fund" class="admin-link">Guthaben hinzufügen</a>
        <a href="/withdraw_fund" class="admin-link">Guthaben abheben</a>
        <h2>Checkout</h2>
        <a href="/checkout_tn" class="admin-link">Teilnehmer auschecken</a>
    </div>
</body>

</html>'

files["add_buy.html"]='<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kauf hinzufügen</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>
<style type="text/css">
    .productBarcodeInput {
        display: none;

    }

    .productBarcodeLabel {
        display: none;
        
    }
</style>
<body>
    <header>
        <h1 class="topic">Kauf</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div>
            <h1>Kauf hinzufügen</h1>
            <p>Scanne den speziellen Barcode "Brake", um den Kauf abzuschließen.</p>
            <form id="buyForm" action="/add_buy" method="post">
                <label for="TN_Barcode" class="participantBarcodeLabel">Teilnehmerbarcode:</label>
                <input id="TN_Barcode" name="TN_Barcode" class="participantBarcodeInput" autofocus autocomplete="off" inputmode="none" autocorrect="off" spellcheck="false">
                <label for="P_Barcode1" class="productBarcodeLabel" style="display:none;">Produktbarcode 1:</label>
                <input id="P_Barcode1" name="P_Barcode1" class="productBarcodeInput" style="display:none;" autocomplete="off" inputmode="none" autocorrect="off" spellcheck="false">
                <label for="P_Barcode2" class="productBarcodeLabel" style="display:none;">Produktbarcode 2:</label>
                <input id="P_Barcode2" name="P_Barcode2" class="productBarcodeInput" style="display:none;" autocomplete="off" inputmode="none" autocorrect="off" spellcheck="false">
                <label for="P_Barcode3" class="productBarcodeLabel" style="display:none;">Produktbarcode 3:</label>
                <input id="P_Barcode3" name="P_Barcode3" class="productBarcodeInput" style="display:none;" autocomplete="off" inputmode="none" autocorrect="off" spellcheck="false">
                <label for="P_Barcode4" class="productBarcodeLabel" style="display:none;">Produktbarcode 4:</label>
                <input id="P_Barcode4" name="P_Barcode4" class="productBarcodeInput" style="display:none;" autocomplete="off" inputmode="none" autocorrect="off" spellcheck="false">
                <label for="P_Barcode5" class="productBarcodeLabel" style="display:none;">Produktbarcode 5:</label>
                <input id="P_Barcode5" name="P_Barcode5" class="productBarcodeInput" style="display:none;" autocomplete="off" inputmode="none" autocorrect="off" spellcheck="false">
                <label for="P_Barcode6" class="productBarcodeLabel" style="display:none;">Produktbarcode 6:</label>
                <input id="P_Barcode6" name="P_Barcode6" class="productBarcodeInput" style="display:none;" autocomplete="off" inputmode="none" autocorrect="off" spellcheck="false">
                <label for="P_Barcode7" class="productBarcodeLabel" style="display:none;">Produktbarcode 7:</label>
                <input id="P_Barcode7" name="P_Barcode7" class="productBarcodeInput" style="display:none;" autocomplete="off" inputmode="none" autocorrect="off" spellcheck="false">
                <input type="submit" value="Kauf hinzufügen">
            </form>
        </div>
    </main>
    <script>
        document.addEventListener('DOMContentLoaded', (event) => {
            let barcodeInputs = ['P_Barcode1', 'P_Barcode2', 'P_Barcode3', 'P_Barcode4', 'P_Barcode5', 'P_Barcode6', 'P_Barcode7'];
            let currentIndex = 0;
            let barcodeInput = '';
            const SPECIAL_BARCODE = 'Brake';

            // Hide all product barcode input fields and their labels initially
            barcodeInputs.forEach(id => {
                document.getElementById(id).style.display = 'none';
                document.querySelector(`label[for=${id}]`).style.display = 'none';
            });

            // Show the first product barcode input field
            document.getElementById(barcodeInputs[currentIndex]).style.display = 'flex';
            document.querySelector(`label[for=${barcodeInputs[currentIndex]}]`).style.display = 'flex';

            // Listen for keypress events on the document
            document.addEventListener('keypress', function (e) {
                if (e.key === 'Enter') {
                    e.preventDefault();

                    if (currentIndex === 0 && e.target.id === 'TN_Barcode') {
                        // Move focus to the first product barcode input field
                        document.getElementById(barcodeInputs[currentIndex]).style.display = 'block';
                        document.querySelector(`label[for=${barcodeInputs[currentIndex]}]`).style.display = 'block';
                        document.getElementById(barcodeInputs[currentIndex]).focus();
                        barcodeInput = ''; // Reset barcode input
                    } else {
                        // Set the current input field with the scanned barcode value
                        document.getElementById(barcodeInputs[currentIndex]).value = barcodeInput;
                        if (barcodeInput === SPECIAL_BARCODE) {
                            document.getElementById(barcodeInputs[currentIndex]).value = ''; // Clear the special barcode
                            // Submit the form if the special barcode is scanned
                            document.getElementById('buyForm').submit();
                        } 
                        else {
                            barcodeInput = ''; // Reset barcode input
                            currentIndex++;

                            if (currentIndex < barcodeInputs.length) {
                                document.getElementById(barcodeInputs[currentIndex]).style.display = 'block';
                                document.querySelector(`label[for=${barcodeInputs[currentIndex]}]`).style.display = 'block';
                                document.getElementById(barcodeInputs[currentIndex]).focus();
                            }
                        }
                    }
                } else {
                    // Append the character to the barcode input
                    barcodeInput += e.key;
                }
            });
        });
    </script>
</body>
</html>'

files["add_fund.html"]='<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Einzahlung hinzufügen</title>
    <link rel="stylesheet" type="text/css" href="/static/styles.css">
</head>

<body>
    <header>
        <h1 class="topic">Guthaben hinzufügen</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="/watch">Übersicht</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div>
            <form method="post">
                <label for="user">Teilnehmername:</label>
                <select id="user" name="user">
                    {% for user in users %}
                    <option value="{{ user }}">{{ user }}</option>
                    {% endfor %}
                </select><br>
                <label for="amount">Betrag:</label>
                <input type="number" id="amount" name="amount" required step="0.01"><br>
                <button class="bt" type="submit">Hinzufügen</button>
            </form>
        </div>
    </main>
</body>

</html>'


files["add_product.html"]='
<!--Filename = add_product.html-->

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Produkt hinzufügen</title>
    <link rel="stylesheet" type="text/css" href="/static/styles.css">
</head>

<body>
    <header>
        <h1 class="topic">Produkt hinzufügen</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="/watch">Übersicht</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div>

            <form method="post">
                <label for="product">Produktname:</label>
                <input type="text" id="product" name="product" placeholder="Produktname" required><br>
                <label for="barcode">Produktbarcode:</label>
                <input type="text" id="P_barcode" name="P_barcode" placeholder="Produktbarcode" required><br>
                <label for="price">Preis:</label>
                <input type="number" id="price" name="price" required placeholder="Preis" step="0.01"><br>
                <button class="bt" type="submit">Hinzufügen</button>
            </form>
        </div>
    </main>
</body>

</html>'

files["add_user.html"]='
<!--Filename = add_user.html-->

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nutzer hinzufügen</title>
    <link rel="stylesheet" type="text/css" href="/static/styles.css">

</head>

<body>
    <header>
        <h1 class="topic">Teilnehmer hinzufügen</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="/watch">Übersicht</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div>
            <form method="post">
                <label for="user">Teilnehmername:</label>
                <input type="text" id="user" name="user" required autofocus><br>
                <label for="barcode">Teilnehmerbarcode:</label>
                <input type="text" id="TN_B" name="TN_B" required><br> <!-- Korrektur: name auf 'TN_B' geändert -->
                <label for="amount">Einzahlungsbetrag:</label>
                <input type="number" id="amount" name="amount" required step="0.01"><br>
                <button class="bt" type="submit">Hinzufügen</button>
            </form>
        </div>
        <main>
</body>

</html>'


files["admin.html"]='
<!--Filename = admin.html-->

<!DOCTYPE html>
<html lang="de">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin Panel</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>

<body>
    <header>
        <h1 class="topic">Admin Panel</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <div class="admin-content">
        <div class="category">
            <h2></h2>
            <a href="/settings" class="admin-link">Einstellungen</a>
            <a href="/teilnehmer" class="admin-link">Teilnehmer</a>
            <a href="/produkte" class="admin-link">Produkte</a>
            <a href="/statistik" class="admin-link">Statistik</a>
            <a href="/dblogin" class="admin-link">Datenbankverwaltung</a>
        </div>
    </div>

</body>

</html>'

files["backup.html"]='
<!--Filename = backup.html-->

<!DOCTYPE html>
<html lang="de">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Datenbank-Backup</title>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap">
    <link rel=stylesheet href="/static/styles.css">
</head>

<body>
    <header>
        <h1 class="topic">Datenbank-Backup</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="/watch">Übersicht</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div class="container">
            <form method="POST">
                <label for="backup_directory">Backup-Verzeichnis:</label>
                <label for="att_backupdir"> {{ backup_directory }} </label>
                <br>
                <br>

                <label for="backup_filename">Backup-Verzeichnis ändern:</label>
                <input type="text" id="backup_directory" name="backup_directory" value="">

                <button class="bt" type="submit">Backup-Verzeichnis ändern</button>
                <br>
                <br>
                <label for="backup_filename">Backup-Dateiname:</label>
                <label for="att_backupfile"> {{ backup_filename }} </label>
                <br>
                <br>
                <button class="bt" type="submit">Backup erstellen</button>


            </form>
        </div>
    </main>
</body>

</html>'


files["buy_check.html"]='
<!--Filename = buy_check.html-->

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kauf Übersicht</title>
    <link rel="stylesheet" href="/static/styles.css">
</head>

<body>
    <header>
        <h1 class="topic">Kauf Übersicht</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Neuen Kauf hinzufügen</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div class="container">
            <h2>Vielen Dank für Ihren Kauf!</h2>
            <p>Teilnehmerbarcode: {{ username }}</p>
            <h3>Gekaufte Produkte:</h3>
            <ul>
                {% for product in products %}
                <li class="li">{{ product }}</li>
                {% endfor %}
            </ul>
            <a href="/add_buy" class="bt">Weiteren Kauf hinzufügen</a>
        </div>
    </main>
</body>

</html>'


files["checkout_c.html"]='
<!--Filename = checkout_c.html-->


<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>Checkout Status</title>
  <link rel="stylesheet" type="text/css" href="/static/styles.css">
  <style>
    .formbt {
      text-align: center;
      border: none;
      border-radius: 5px;
      padding: 5px;
      cursor: pointer;
      display: block;
      margin: 10px auto;
    }
  </style>
</head>

<body>
  <header>
    <h1 class="topic">Checkout Status</h1>
    <nav>
      <ul>
        <li><a href="/add_user">Nutzer hinzufügen</a></li>
        <li><a href="/watch">Auswertung</a></li>
        <li><a href="/admin">Einstellungen</a></li>
      </ul>
    </nav>
  </header>
  <main>
    <div class="container">


      <p>Benutzer: {{ benutzer_id }}</p>
      <p>Kontostand: {{ kontostand }} €</p>
      <h2>Benötigte Geldaufteilung</h2>
      <ul>
        {% for denom, count in counts.items() %}
        <li class="li">{{ denom }}€: {{ count }}x</li>
        {% endfor %}
      </ul>
      <form class="formbt" method="post" action="{{ url_for('confirm_checkout') }}">
        <input type="hidden" name="user" value="{{ benutzer_id }}">
        <button class="bt" type="submit">Checkout bestätigen</button>
      </form>
    </div>
  </main>
</body>

</html>'

files["delete_database.html"]='
<!--Filename = delete_database.html-->
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Datenbank löschen</title>
    <link rel="stylesheet" type="text/css" href="/static/styles.css">
</head>

<body>
    <header>
        <h1 class="topic">Datenbank löschen <h1>
                <nav>
                    <ul>
                        <li><a href="/open_barcode">Barcode-Transaktionen</a></li>
                        <li><a href="/add_user">Nutzer hinzufügen</a></li>
                        <li><a href="/watch">Auswertung</a></li>
                        <li><a href="#" onclick="history.back();">Zurück</a>
                        <li>
                    </ul>
                </nav>
    </header>
    <div>
        <h1>Datenbank auswählen</h1>
        <form method="post">
            <label for="password">Passwort:</label>
            <input type="password" id="password" name="password" required><br>
            <button type="submit">Löschen</button>
        </form>
    </div>
</body>

</html>'

files["edit_product_prices.html"]='
<!--Filename = edit_product_prices.html-->

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Produktpreise bearbeiten</title>
    <link rel="stylesheet" type="text/css" href="/static/styles.css">
    <script>
        function confirmDelete() {
            return confirm("Sind Sie sicher, dass Sie dieses Produkt löschen möchten?");
        }
    </script>
</head>

<body>
    <header>
        <h1 class="topic">Produktpreise bearbeiten</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="/watch">Übersicht</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div>
            <h1>Produkt bearbeiten</h1>
            <form method="post" action="{{ url_for('edit_product_prices') }}">
                <label for="selected_product">Produktname:</label>
                <select id="selected_product" name="selected_product">
                    {% for product in products %}
                    <option value="{{ product }}">{{ product }}</option>
                    {% endfor %}
                </select><br>
                <label for="new_price">Neuer Preis:</label>
                <input type="text" id="new_price" name="new_price" placeholder="Preis"><br>
                <label for="new_barcode">Neuer Barcode:</label>
                <input type="text" id="new_barcode" name="new_barcode" placeholder="Barcode"><br>
                <button class="bt" type="submit" name="action" value="update_barcode">Aktualisiere Barcode</button>
                <button class="bt" type="submit" name="action" value="update">Aktualisieren</button>
                <button class="bt" type="submit" name="action" value="delete" onclick="return confirmDelete();">Produkt
                    löschen</button>
            </form>
        </div>
    </main>
</body>

</html>'

files["edit_user.html"]='
<!--Filename = edit_user.html-->

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Nutzer bearbeiten</title>
    <link rel="stylesheet" type="text/css" href="/static/styles.css">
    <script>
        function confirmDelete() {
            return confirm("Sind Sie sicher, dass Sie diesen Benutzer löschen möchten?");
        }
    </script>
</head>

<body>
    <header>
        <h1 class="topic">Benutzer bearbeiten</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="/watch">Übersicht</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div>
            <form method="post" action="{{ url_for('edit_user') }}">
                <label for="selected_user">Aktueller Teilnehmername:</label>
                <select id="selected_user" name="selected_user">
                    {% for user in users %}
                    <option value="{{ user }}">{{ user }}</option>
                    {% endfor %}
                </select><br>
                <label for="new_name">Neuer Teilnehmername:</label>
                <input type="text" id="new_name" name="new_name" placeholder="Neuer Teilnehmername"><br>
                <label for="new_barcode">Neuer Teilnehmerbarcode:</label>
                <input type="text" id="new_barcode" name="new_barcode" placeholder="Neuer Teilnehmerbarcode"><br>
                <button class="bt" type="submit" name="action" value="update">Aktualisiere Name</button>
                <button class="bt" type="submit" name="action" value="update_b">Aktualisiere Barcode</button>
                <button class="bt" type="submit" name="action" value="delete" onclick="return confirmDelete();">Benutzer
                    löschen</button>
            </form>
        </div>
    </main>
</body>

</html>'

files["index.html"]='
<!-- Filename = index.html -->

<!DOCTYPE html>
<html lang="de">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ titel }} Bankings</title>
    <!--<link rel="stylesheet" href="/static/styles.css">-->
    <style>
        /* CSS-Design für die Navigation */
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
        }

        header {
            text-align: center;
            padding: 20px 0;
            background-color: #333;
            color: white;
        }

        nav ul {
            list-style: none;
            padding: 0;
            text-align: center;
        }

        nav ul li {
            display: inline;
            margin-right: 20px;
        }

        nav ul li:last-child {
            margin-right: 0;
        }

        nav ul li a {
            text-decoration: none;
            padding: 10px 20px;
            background-color: #ff004d;
            color: white;
            border: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }

        nav ul li a:hover {
            background-color: #ff1a66;
            color: black;
        }

        @media (max-width: 768px) {
            nav ul {
                flex-direction: column;
                margin: 0;
                padding: 0;
            }

            nav ul li {
                display: block;
                margin: 1px 0;
            }

            li {
                margin: 2px;
            }

            a {
                margin: 5px;
                display: block;
            }
        }
    </style>
    <script>
        // JavaScript-Code, um die Login-Seite anzuzeigen
        window.onload = function () {
            var settingsLink = document.querySelector('a[href="/admin"]');
            settingsLink.onclick = function (event) {
                event.preventDefault();
                window.location.href = '/login';
            };
        };
    </script>
</head>

<body>
    <header>
        <h1 class="topic">{{ titel }} Bankings</h1>
    </header>
    <nav>
        <ul>
            <li><a href="/add_buy">Kauf</a></li>
            <!--<li><a href="/watch">Auswertung</a></li>-->
            <li><a href="/admin">Einstellungen</a></li>
        </ul>
    </nav>
</body>

</html>'


files["kaufstatistik.html"]='
<!--Filename = kaufstatistik.html-->

<!DOCTYPE html>
<html lang="de">

<head>
    <meta charset="UTF-8">
    <title>Kaufstatistik</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/styles.css">
</head>

<body onload="reloadFunction()">
    <header>
        <h1 class="topic">Kaufstatistik</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="/watch">Übersicht</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div class="kaufstatiskik">
            <h2>Kaufstatistik</h2>
            <table class="table table-striped">
                <thead>
                    <tr>
                        {% for col in data[0].keys() %}
                        <th>{{ col }}</th>
                        {% endfor %}
                    </tr>
                </thead>
                <tbody>
                    {% for row in data %}
                    <tr>
                        {% for value in row.values() %}
                        <td>{{ value }}</td>
                        {% endfor %}
                    </tr>
                    {% endfor %}
                </tbody>
            </table>
        </div>
    </main>
</body>

</html>'

files["login.html"]='
<!--Filename = login.html-->

<!DOCTYPE html>
<html lang="de">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" type="text/css" href="/static/styles.css">
</head>

<body>
    <header>
        <h1 class="topic">Admin Login</h1>
    </header>
    <form method="post">
        <label for="password">Passwort:</label>
        <input type="password" id="password" name="password" required>
        <button class="bt" type="submit">Einloggen</button>
    </form>
</body>

</html>'

files["loginform.html"]='
<!--Filename = loginform.html-->

<!DOCTYPE html>
<html lang="de">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login</title>
    <link rel="stylesheet" type="text/css" href="/static/styles.css">
</head>

<body>
    <header>
        <h1 class="topic">Admin Login</h1>
    </header>
    <form method="post">
        <label for="password">Passwort:</label>
        <input type="password" id="passworddb" name="passworddb" required>
        <button class="bt" type="submit">Einloggen</button>
    </form>
</body>

</html>'

files["results.html"]='
<!--Filename = results.html-->

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Geld Aufteilen</title>
    <link rel="stylesheet" type="text/css" href="/static/styles.css">
</head>

<body>
    <header>
        <h1 class="topic">Geld Aufteilen</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="/watch">Übersicht</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div class="container">
            <ul>
                {% for denom, count in results.counts.items() %}
                <li class="li">{{ denom }} €: {{ count }}x</li>
                {% endfor %}
                <li class="highlight">Summe: {{ results.sume | round(2) }} €</li>
                <li class="highlight">Gesamt Kontostand: {{ results.gesamt_kontostand | round(2) }} €</li>
            </ul>
        </div>
    </main>
</body>

</html>
'
files["settings.html"]='
<!--Filename = settings.html-->

<!DOCTYPE html>
<html lang="de">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Einstellungen</title>
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
    <link rel="stylesheet" href="/static/styles.css">
</head>

<body>
    <header>
        <h2 class="topic">Einstellungen</h2>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="/watch">Übersicht</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div class="container mt-5">
            <form id="date_form" action="/settings" method="POST">
                <div class="form-group">
                    <label for="lagername">Lagername:</label>
                    <input type="text" class="form-control" id="lagername" name="lagername" value="{{ lagername }}">
                </div>
                <div class="form-group">
                    <label for="first_day">Erster Tag:</label>
                    <input type="date" class="form-control" id="first_day" name="first_day" value="{{ first_day }}">
                </div>
                <div class="form-group">
                    <label for="last_day">Letzter Tag:</label>
                    <input type="date" class="form-control" id="last_day" name="last_day" value="{{ last_day }}">
                </div>
                <input type="hidden" id="formatted_first_day" name="formatted_first_day">
                <input type="hidden" id="formatted_last_day" name="formatted_last_day">
                <button class="bt" type="submit">Speichern</button>
            </form>
            <hr>
            <div>
                <h4>Aktuelle Einstellungen</h4>
                <p>Lagername: {{lagername}}</p>
                <p>Startdatum: {{ first_day }}</p>
                <p>Lagerdauer: {{ lager_dauer }} Tage</p>
                <p>Enddatum: {{ last_day }}</p>
                <p>Heute: {{ today }}</p>
            </div>
        </div>
    </main>
    <script>
        document.getElementById('date_form').addEventListener('submit', function (event) {
            var firstDayInput = document.getElementById('first_day').value;
            var lastDayInput = document.getElementById('last_day').value;
            var lagernameInput = document.getElementById('lagername').value;

            if (firstDayInput) {
                var firstDayParts = firstDayInput.split('-');
                var formattedFirstDay = firstDayParts[2] + '-' + firstDayParts[1] + '-' + firstDayParts[0];
                document.getElementById('formatted_first_day').value = formattedFirstDay;
            }

            if (lastDayInput) {
                var lastDayParts = lastDayInput.split('-');
                var formattedLastDay = lastDayParts[2] + '-' + lastDayParts[1] + '-' + lastDayParts[0];
                document.getElementById('formatted_last_day').value = formattedLastDay;
            }
        });
    </script>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.5.4/dist/umd/popper.min.js"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>

</html>
'
files["Abfrage.html"]='
<!--Filename = TN-Abfrage.html-->

<!doctype html>
<html lang="en">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
  <title>Checkout System</title>
  <link rel="stylesheet" type="text/css" href="/static/styles.css">
</head>

<body>
  <header>
    <h1 class="topic">Teilnehmer auschecken</h1>
    <nav>
      <ul>
        <li><a href="/">Startseite</a></li>
        <li><a href="/add_buy">Kauf hinzufügen</a></li>
        <li><a href="/watch">Auswertung</a></li>
        <li><a href="/admin">Einstellungen</a></li>
        <li><a href="#" onclick="history.back();">Zurück</a></li>
      </ul>
    </nav>
  </header>
  <main>
    <div class="">
      <h1>Teilnehmer auswählen</h1>
      <form action="{{ url_for('checkout') }}" method="post">
        <select name="user">
          {% for user in users %}
          <option value="{{ user }}">{{ user }}</option>
          {% endfor %}
        </select>
        <button class="bt" type="submit">Checkout</button>
      </form>
    </div>
  </main>
</body>

</html>
'
files["watch.html"]='
<!--Filename = watch.html-->

<!DOCTYPE html>
<html lang="de">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Transaktionen anzeigen</title>
    <link rel="stylesheet" href="https://cdn.datatables.net/1.10.21/css/jquery.dataTables.min.css">

    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f5f5f5;
            margin: 0;
            padding: 0;
            display: flex;
            flex-direction: column;
            height: 100vh;
            height: 100%;
            justify-content: center;
            align-items: center;
        }

        header {
            width: 100%;
            text-align: center;
            padding: 20px 0;
            background-color: #333;
            color: white;
        }

        nav ul {
            list-style: none;
            padding: 0;
            text-align: center;
            margin: 0;
        }

        nav ul li {
            display: inline;
            margin-right: 20px;
        }

        nav ul li:last-child {
            margin-right: 0;
        }

        nav ul li a {
            text-decoration: none;
            padding: 10px 20px;
            background-color: #ff004d;
            color: white;
            border: none;
            border-radius: 5px;
            transition: background-color 0.3s;
        }

        nav ul li a:hover {
            background-color: #ff1a66;
            color: black;
        }

        main {
            flex: 1;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            padding: 20px;
        }

        a {
            display: column;
            text-align: center;
            margin-top: 20px;
            color: #333;
            text-decoration: none;
        }

        button {
            padding: 10px 20px;
            background-color: #ff004d;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            margin: 10px 0;
            transition: background-color 0.3s;
        }

        button:hover {
            background-color: #ff1a66;
            color: black;
        }

        @media (max-width: 768px) {
            nav ul {
                flex-direction: column;
                margin: 0;
                padding: 0;
            }

            nav ul li {
                display: block;
                margin: 1px 0;
            }

            li {
                margin: 2px;
            }

            a {
                margin: 5px;
                display: block;
            }
        }
    </style>
</head>

<body>
    <header>
        <h1 class="topic">Transaktionen anzeigen</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="/backup">Backup</a></li>

            </ul>
        </nav>
    </header>
    <main>
        <div> <!-- Hinzugefügt: horizontaler Scroll -->
            {{ tables|safe }}
        </div>
    </main>
    <script src="https://code.jquery.com/jquery-3.5.1.min.js"></script>
    <script src="https://cdn.datatables.net/1.10.21/js/jquery.dataTables.min.js"></script>
    <script>
        $(document).ready(function () {
            $('table.data').DataTable({
                "paging": false,  // Disable pagination
                "searching": true
            });
        });
    </script>
</body>

</html>
'
files["withdraw_fund.html"]='
<!--Filename = withdraw_fund.html-->

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Guthaben abheben</title>
    <link rel="stylesheet" type="text/css" href="/static/styles.css">
</head>

<body>
    <header>
        <h1 class="topic">Guthaben abheben</h1>
        <nav>
            <ul>
                <li><a href="/">Startseite</a></li>
                <li><a href="/add_buy">Kauf hinzufügen</a></li>
                <li><a href="/watch">Übersicht</a></li>
                <li><a href="#" onclick="history.back();">Zurück</a></li>
            </ul>
        </nav>
    </header>
    <main>
        <div>
            <form method="post">
                <label for="user">Teilnhemername:</label>
                <select id="user" name="user">
                    {% for user in users %}
                    <option value="{{ user }}">{{ user }}</option>
                    {% endfor %}
                </select><br>
                <label for="amount">Betrag:</label>
                <input type="number" id="amount" name="amount" required step="0.01"><br>
                <button class="bt" type="submit">Abheben</button>
            </form>
        </div>
    </main>
</body>

</html>
'
files["loginform.html"]='

'
###########################################################################


# Create the files with the respective contents
for filename in "${!files[@]}"; do
    echo "Creating $directory/$filename"
    echo "${files[$filename]}" > "$directory/$filename"
done

echo "All files have been created successfully!"


# sudo chmod +x create_html_files.sh


# sudo ./create_html_files.sh

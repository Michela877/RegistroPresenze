from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from datetime import datetime
import os  # Importa il modulo os

app = Flask(__name__, template_folder='templates')

# Configurazione del database MySQL
db = mysql.connector.connect(
    host=os.environ.get('DB_HOST'),
    user=os.environ.get('DB_USER'),
    password=os.environ.get('DB_PASSWORD'),
    database=os.environ.get('DB_NAME')
)

def get_current_time():
    # Funzione per ottenere l'orario attuale come stringa nel formato HH:MM
    now = datetime.now()
    return now.strftime("%H:%M")

def get_current_date():
    # Funzione per ottenere la data attuale come stringa nel formato YYYY-MM-DD
    today = datetime.today()
    return today.strftime("%Y-%m-%d")

@app.route('/')
def index():
    # Ottenere l'orario di entrata attuale e la data attuale
    orario_entrata = get_current_time()
    data_presenza = get_current_date()
    
    # Ottenere l'orario di uscita attuale
    orario_uscita = get_current_time()
    
    # Mostra tutte le presenze registrate
    cursor = db.cursor()
    cursor.execute("SELECT presenze.id, utenti.nome, presenze.data_presenza, presenze.orario_entrata, presenze.orario_uscita FROM presenze JOIN utenti ON presenze.nome = utenti.id")
    presenze = cursor.fetchall()

    # Ottenere tutti gli utenti
    cursor.execute("SELECT id, nome FROM utenti")
    utenti = cursor.fetchall()

    cursor.close()
    
    return render_template('index.html', presenze=presenze, orario_entrata=orario_entrata, data_presenza=data_presenza, orario_uscita=orario_uscita, utenti=utenti)

@app.route('/aggiungi_entrata', methods=['POST'])
def aggiungi_entrata():
    # Ottieni i dati dal form
    utente_id = request.form['utente']
    data_presenza = request.form['data_presenza']
    orario_entrata = request.form['orario_entrata']

    # Controlla se esiste già una registrazione per lo stesso utente e data corrente
    cursor = db.cursor()
    cursor.execute("SELECT id FROM presenze WHERE nome = %s AND data_presenza = %s", (utente_id, data_presenza))
    result = cursor.fetchone()

    if result:
        # Se esiste già una registrazione per il giorno corrente, aggiorna l'orario di entrata
        cursor.execute("UPDATE presenze SET orario_entrata = %s WHERE id = %s", (orario_entrata, result[0]))
    else:
        # Altrimenti, inserisci una nuova registrazione
        cursor.execute("INSERT INTO presenze (nome, data_presenza, orario_entrata) VALUES (%s, %s, %s)",
                       (utente_id, data_presenza, orario_entrata))

    db.commit()
    cursor.close()

    # Reindirizza alla homepage
    return redirect(url_for('index'))

@app.route('/aggiungi_uscita', methods=['POST'])
def aggiungi_uscita():
    # Ottieni i dati dal form
    utente_id = request.form['utente']
    data_presenza = request.form['data_presenza']
    orario_uscita = get_current_time()  # Calcola l'orario di uscita nel backend

    # Controlla se esiste già una registrazione per lo stesso utente e data corrente
    cursor = db.cursor()
    cursor.execute("SELECT id FROM presenze WHERE nome = %s AND data_presenza = %s", (utente_id, data_presenza))
    result = cursor.fetchone()

    if result:
        # Se esiste già una registrazione per il giorno corrente, aggiorna l'orario di uscita
        cursor.execute("UPDATE presenze SET orario_uscita = %s WHERE id = %s", (orario_uscita, result[0]))
    else:
        # Altrimenti, inserisci una nuova registrazione con solo l'orario di uscita
        cursor.execute("INSERT INTO presenze (nome, data_presenza, orario_uscita) VALUES (%s, %s, %s)",
                       (utente_id, data_presenza, orario_uscita))

    db.commit()
    cursor.close()

    # Reindirizza alla homepage
    return redirect(url_for('index'))

@app.route('/aggiungi_utente', methods=['GET', 'POST'])
def aggiungi_utente():
    if request.method == 'POST':
        # Ottieni i dati dal form
        nome = request.form['nome']
        
        # Inserisci il nuovo utente nel database
        cursor = db.cursor()
        cursor.execute("INSERT INTO utenti (nome) VALUES (%s)", (nome,))
        db.commit()
        cursor.close()
        
        # Reindirizza alla homepage dopo l'aggiunta dell'utente
        return redirect(url_for('index'))
    else:
        # Se la richiesta è GET, mostra il form per l'aggiunta di un nuovo utente
        return render_template('aggiungi_utente.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6001)
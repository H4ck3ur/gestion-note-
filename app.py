from flask import Flask, request
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    conn = sqlite3.connect('notes_ecole.db')
    c = conn.cursor()
    
    # Table élèves
    c.execute('CREATE TABLE IF NOT EXISTS eleves (id INTEGER PRIMARY KEY AUTOINCREMENT, nom TEXT, prenom TEXT)')
    
    # NOUVELLE table notes
    c.execute('CREATE TABLE IF NOT EXISTS notes (id INTEGER PRIMARY KEY AUTOINCREMENT, eleve_id INTEGER, matiere TEXT, note REAL)')
    
    # Ajoute élève
    if request.form.get('nom'):
        nom = request.form['nom']
        prenom = request.form['prenom']
        c.execute("INSERT INTO eleves (nom, prenom) VALUES (?, ?)", (nom, prenom))
        conn.commit()
    
    # Ajoute note
    if request.form.get('eleve_id'):
        eleve_id = request.form['eleve_id']
        matiere = request.form['matiere']
        note = request.form['note']
        c.execute("INSERT INTO notes (eleve_id, matiere, note) VALUES (?, ?, ?)", (eleve_id, matiere, note))
        conn.commit()
    
    # Liste élèves
    c.execute("SELECT id, nom, prenom FROM eleves")
    eleves = c.fetchall()
    
    # Liste notes
    c.execute("SELECT e.nom, e.prenom, n.matiere, n.note FROM notes n JOIN eleves e ON n.eleve_id = e.id")
    notes = c.fetchall()
    
    html = '<h1>📚 Gestion école</h1>'
    
    # Élèves
    html += '<h2>👥 Élèves</h2><ul>'
    for id, nom, prenom in eleves:
        html += f'<li>ID{id}: {nom} {prenom}</li>'
    html += '</ul>'
    
    # Formulaire élèves
    html += '<h3>Ajouter élève</h3><form method=post><input name=nom placeholder="Nom"> <input name=prenom placeholder="Prénom"> <button>Ajouter élève</button></form>'
    
    # Notes
    html += '<h2>📝 Notes</h2><ul>'
    for nom, prenom, matiere, note in notes:
        html += f'<li>{nom} {prenom}: {matiere} = {note}/20</li>'
    html += '</ul>'
    
    # Formulaire notes (menu déroulant élèves)
    html += '<h3>Ajouter note</h3><form method=post>'
    html += '<select name=eleve_id>'
    for id, nom, prenom in eleves:
        html += f'<option value="{id}">{nom} {prenom}</option>'
    html += '</select> '
    html += '<input name=matiere placeholder="Matière"> '
    html += '<input name=note placeholder="Note" type=number step=0.1 max=20> '
    html += '<button>Ajouter note</button></form>'
    
    conn.close()
    return html

if __name__ == '__main__':
    app.run(debug=True)

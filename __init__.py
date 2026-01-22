import sqlite3
from flask import Flask, render_template, request, url_for, flash, redirect

app = Flask(__name__)
app.config['SECRET_KEY'] = 'votre_cle_secrete_ici'

def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

# 1. Page d'accueil : Afficher les tâches [cite: 7, 13]
@app.route('/')
def index():
    conn = get_db_connection()
    # On récupère toutes les tâches
    taches = conn.execute('SELECT * FROM taches').fetchall()
    conn.close()
    return render_template('index.html', taches=taches)

# 2. Ajouter une tâche [cite: 6, 13]
@app.route('/ajouter', methods=('GET', 'POST'))
def ajouter():
    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        date = request.form['date_echeance']

        if not titre:
            flash('Le titre est obligatoire!')
        else:
            conn = get_db_connection()
            conn.execute('INSERT INTO taches (titre, description, date_echeance) VALUES (?, ?, ?)',
                         (titre, description, date))
            conn.commit()
            conn.close()
            return redirect(url_for('index'))
           
    return render_template('ajouter.html')

# 3. Supprimer une tâche
@app.route('/supprimer/<int:id>', methods=('POST',))
def supprimer(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM taches WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    flash('Tâche supprimée!')
    return redirect(url_for('index'))

# 4. Marquer comme terminée
@app.route('/terminer/<int:id>', methods=('POST',))
def terminer(id):
    conn = get_db_connection()
    # On met à jour le statut à 1 (Vrai)
    conn.execute('UPDATE taches SET est_terminee = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

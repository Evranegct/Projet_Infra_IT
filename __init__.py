from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)                                                                                                                                                                                                                                    
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/' 

# --- ROUTES DE LA BIBLIOTHÈQUE ---

@app.route('/')
def home():
    return "<h1>Bienvenue à la Bibliothèque</h1><p>Allez sur /consultation/ pour voir les livres.</p>"

# 1. Consulter tous les livres
@app.route('/consultation/')
def consulter_livres():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres;') # On utilise la nouvelle table
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

# 2. Enregistrer un nouveau livre
@app.route('/ajouter_livre', methods=['GET', 'POST'])
def ajouter_livre():
    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO livres (titre, auteur) VALUES (?, ?)', (titre, auteur))
        conn.commit()
        conn.close()
        return redirect(url_for('consulter_livres'))
    return render_template('formulaire_livre.html') # Assure-toi d'avoir ce template

# 3. Rechercher un livre par titre (Adaptation de l'exercice Séquence 5)
@app.route('/recherche/<titre>')
def recherche_livre(titre):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres WHERE titre LIKE ?', ('%' + titre + '%',))
    data = cursor.fetchall()
    conn.close()
    return render_template('read_data.html', data=data)

if __name__ == "__main__":
  app.run(debug=True)

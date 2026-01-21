from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

DATABASE = 'database.db'

# ---------------------------
# FONCTIONS UTILES
# ---------------------------
def get_db():
    return sqlite3.connect(DATABASE)

def est_authentifie():
    return session.get('authentifie') is True


# ---------------------------
# ROUTES PRINCIPALES
# ---------------------------
@app.route('/')
def hello_world():
    return render_template('hello.html')


@app.route('/deconnexion')
def deconnexion():
    session.clear()
    return redirect(url_for('authentification'))


@app.route('/lecture')
def lecture():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    return render_template(
        'lecture.html',
        username=session.get('username'),
        role=session.get('role')
    )


# ---------------------------
# AUTHENTIFICATION
# ---------------------------
@app.route('/authentification', methods=['GET', 'POST'])
def authentification():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # ADMIN
        if username == 'admin' and password == 'password':
            session['authentifie'] = True
            session['username'] = 'admin'
            session['role'] = 'admin'
            return redirect(url_for('lecture'))

        # USER
        elif username == 'user' and password == '12345':
            session['authentifie'] = True
            session['username'] = 'user'
            session['role'] = 'user'
            return redirect(url_for('lecture'))

        else:
            return render_template('formulaire_authentification.html', error=True)

    return render_template('formulaire_authentification.html', error=False)


# ---------------------------
# LIVRES
# ---------------------------
@app.route('/consultation')
def ReadBDD():
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM livres')
    data = cursor.fetchall()
    conn.close()

    return render_template('read_data.html', data=data)


@app.route('/fiche_livre/<titre>')
def fiche_livre(titre):
    if not est_authentifie():
        return redirect(url_for('authentification'))

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT * FROM livres WHERE titre LIKE ?',
        ('%' + titre + '%',)
    )
    data = cursor.fetchall()
    conn.close()

    return render_template('read_data.html', data=data)


@app.route('/enregistrer_livre', methods=['GET', 'POST'])
def enregistrer_livre():
    if not est_authentifie() or session.get('role') != 'admin':
        return "Accès refusé", 403

    if request.method == 'POST':
        titre = request.form['titre']
        auteur = request.form['auteur']
        annee = request.form['annee']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO livres (titre, auteur, annee_publication) VALUES (?, ?, ?)',
            (titre, auteur, annee)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('ReadBDD'))

    return render_template('formulaire_livre.html')


@app.route('/supprimer_livre/<int:id>')
def supprimer_livre(id):
    if not est_authentifie() or session.get('role') != 'admin':
        return "Accès refusé", 403

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM livres WHERE id = ?', (id,))
    conn.commit()
    conn.close()

    return redirect(url_for('ReadBDD'))


# ---------------------------
# CLIENTS
# ---------------------------
@app.route('/ajouter_client', methods=['GET', 'POST'])
def ajouter_client():
    if not est_authentifie() or session.get('role') != 'admin':
        return "Accès refusé", 403

    if request.method == 'POST':
        nom = request.form['nom']
        email = request.form['email']

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO clients (nom, email) VALUES (?, ?)',
            (nom, email)
        )
        conn.commit()
        conn.close()

        return redirect(url_for('lecture'))

    return render_template('formulaire_client.html')


# ---------------------------
# LANCEMENT
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)

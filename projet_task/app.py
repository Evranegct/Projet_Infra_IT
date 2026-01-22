from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

# 1. Afficher les tâches (ACCUEIL)
@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

# 2. Ajouter une tâche
@app.route('/add', methods=('GET', 'POST'))
def add_task():
    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        date_echeance = request.form['date_echeance']

        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (titre, description, date_echeance) VALUES (?, ?, ?)',
                     (titre, description, date_echeance))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    return render_template('add_task.html')

# 3. Marquer comme terminée ou supprimer
@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)

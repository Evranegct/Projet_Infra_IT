from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('tasks.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=('GET', 'POST'))
def add_task():
    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        date_echeance = request.form['date_echeance']

        conn = get_db_connection()
        conn.execute('INSERT INTO tasks (titre, description, date_echeance, terminee) VALUES (?, ?, ?, ?)',
                     (titre, description, date_echeance, 0))
        conn.commit()
        conn.close()
        # CORRECTION ICI : on utilise le nom de la fonction 'index'
        return redirect(url_for('index'))
    return render_template('add_task.html')

@app.route('/complete/<int:id>')
def complete(id):
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET terminee = 1 WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

@app.route('/delete/<int:id>')
def delete(id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

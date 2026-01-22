import sqlite3

connection = sqlite3.connect('tasks.db') # Nom de votre nouvelle base

with open('schema.sql') as f:
    connection.executescript(f.read())

connection.commit()
connection.close()
print("La nouvelle base de données 'tasks.db' a été créée avec succès !")

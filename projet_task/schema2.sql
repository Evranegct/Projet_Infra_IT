DROP TABLE IF EXISTS tasks;

CREATE TABLE tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titre TEXT NOT NULL,
    description TEXT NOT NULL,
    date_echeance TEXT, -- SQLite stocke les dates sous forme de texte (YYYY-MM-DD)
    est_terminee INTEGER DEFAULT 0 -- 0 = En cours, 1 = Terminée
);

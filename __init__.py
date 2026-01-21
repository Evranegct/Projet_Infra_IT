from flask import Flask, render_template, request, redirect, url_for, session
import sqlite3

app = Flask(__name__)
app.secret_key = "cle_secrete_alwaysdata"

DATABASE = "database.db"

# --------------------
# OUTILS
# --------------------
def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row  # IMPORTANT (évite bugs)
    return conn

def est_authentifie():
    return session.get("authentifie") == True


# --------------------
# ROUTE TEST
# --------------------
@app.route("/test")
def test():
    return "SERVEUR OK"


# --------------------
# ACCUEIL
# --------------------
@app.route("/")
def home():
    return render_template("hello.html")


# --------------------
# AUTHENTIFICATION
# --------------------
@app.route("/authentification", methods=["GET", "POST"])
def authentification():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username == "admin" and password == "password":
            session.clear()
            session["authentifie"] = True
            session["username"] = "admin"
            session["role"] = "admin"
            return redirect(url_for("lecture"))

        if username == "user" and password == "12345":
            session.clear()
            session["authentifie"] = True
            session["username"] = "user"
            session["role"] = "user"
            return redirect(url_for("lecture"))

        return render_template("formulaire_authentification.html", error=True)

    return render_template("formulaire_authentification.html", error=False)


@app.route("/deconnexion")
def deconnexion():
    session.clear()
    return redirect(url_for("authentification"))


# --------------------
# PAGE PRINCIPALE
# --------------------
@app.route("/lecture")
def lecture():
    if not est_authentifie():
        return redirect(url_for("authentification"))

    return render_template(
        "lecture.html",
        username=session["username"],
        role=session["role"]
    )


# --------------------
# CONSULTATION DES LIVRES (CORRIGÉE)
# --------------------
@app.route("/consultation")
def consultation():
    if not est_authentifie():
        return redirect(url_for("authentification"))

    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM livres")
        livres = cursor.fetchall()

        conn.close()

        return render_template("read_data.html", data=livres)

    except Exception as e:
        # Affiche l’erreur directement (AlwaysData friendly)
        return f"<h1>Erreur consultation</h1><pre>{e}</pre>"


# --------------------
# AJOUT LIVRE
# --------------------
@app.route("/ajouter_livre", methods=["GET", "POST"])
def ajouter_livre():
    if not est_authentifie() or session["role"] != "admin":
        return "Accès refusé", 403

    if request.method == "POST":
        titre = request.form.get("titre")
        auteur = request.form.get("auteur")
        annee = request.form.get("annee")

        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO livres (titre, auteur, annee_publication) VALUES (?, ?, ?)",
            (titre, auteur, annee)
        )
        conn.commit()
        conn.close()

        return redirect(url_for("consultation"))

    return render_template("formulaire_livre.html")


# --------------------
# SUPPRESSION LIVRE
# --------------------
@app.route("/supprimer_livre/<int:id>")
def supprimer_livre(id):
    if not est_authentifie() or session["role"] != "admin":
        return "Accès refusé", 403

    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM livres WHERE id = ?", (id,))
    conn.commit()
    conn.close()

    return redirect(url_for("consultation"))


# --------------------
# LANCEMENT
# --------------------
if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")

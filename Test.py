from flask import Flask, render_template, request,redirect, url_for
import mysql.connector

app = Flask(__name__)

# Configuration de la connexion à la base de données
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'mon_app',
    'port': 3306,
}

@app.route("/Connexion.html", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Connexion à la base de données
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()

        # Exécution de la requête SQL
        cur.execute("SELECT * FROM Utilisateur WHERE Email = %s AND Password = %s", (email, password))
        user = cur.fetchone()

        # Fermeture du curseur et de la connexion
        cur.close()
        conn.close()

        if user:
            return redirect(url_for('afficher_taches'))
        else:
            return "Invalid email or password. Please try again."

    return render_template('Connexion.html')


@app.route("/Inscription.html", methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nom = request.form['nom']
        prenom = request.form['prenom']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']
        telephone = request.form['telephone']

        if password != confirm_password:
            return "Les mots de passe ne correspondent pas. Veuillez réessayer."

        # Connexion à la base de données
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()

        # Exécution de la requête SQL
        cur.execute("INSERT INTO mon_app.Utilisateur (Nom, Prénom, Email, Password, Téléphone) VALUES (%s, %s, %s, %s, %s)", (nom, prenom, email, password, telephone))

        # Validation de la transaction
        conn.commit()

        # Fermeture du curseur et de la connexion
        cur.close()
        conn.close()

        return redirect(url_for('login'))
    return render_template('Inscription.html')


@app.route("/Tache.html", methods=['GET', 'POST'])
def ajouter_tache():
    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        statue = request.form['statue']


        # Connexion à la base de données
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()

        # Exécution de la requête SQL
        cur.execute("INSERT INTO mon_app.Tâche (Titre, Description, Statue) VALUES (%s, %s, %s)", (titre, description, statue))

        # Validation de la transaction
        conn.commit()

        # Fermeture du curseur et de la connexion
        cur.close()
        conn.close()

        return redirect(url_for('afficher_taches'))
    return render_template('Tache.html')

@app.route("/taches", methods=['GET'])
def afficher_taches():
    # Connexion à la base de données
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()

    # Exécution de la requête SQL pour récupérer les tâches
    cur.execute("SELECT * FROM mon_app.Tâche")
    taches = cur.fetchall()

    # Fermeture du curseur et de la connexion
    cur.close()
    conn.close()

    # Affichage des tâches dans un template
    return render_template('taches.html', taches=taches)

@app.route("/supprimer/<int:id_tache>", methods=['GET'])
def supprimer_tache(id_tache):
    # Connexion à la base de données
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()

    # Exécution de la requête SQL pour supprimer la tâche
    cur.execute("DELETE FROM mon_app.Tâche WHERE Id_tache = %s", (id_tache,))

    # Validation de la transaction
    conn.commit()

    # Fermeture du curseur et de la connexion
    cur.close()
    conn.close()

    # Redirection vers la page des tâches après la suppression
    return redirect("/taches")


@app.route("/modifier/<int:id_tache>", methods=['GET', 'POST'])
def modifier_tache(id_tache):
    if request.method == 'POST':
        titre = request.form['titre']
        description = request.form['description']
        statue = request.form['statue']

        # Connexion à la base de données
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()

        # Exécution de la requête SQL pour modifier la tâche
        cur.execute("UPDATE mon_app.Tâche SET Titre = %s, Description = %s, Statue = %s WHERE Id_tache = %s", (titre, description, statue, id_tache))

        # Validation de la transaction
        conn.commit()

        # Fermeture du curseur et de la connexion
        cur.close()
        conn.close()

        # Redirection vers la page des tâches après la modification
        return redirect("/taches")

    # Récupérer les informations de la tâche à modifier
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()
    cur.execute("SELECT * FROM mon_app.Tâche WHERE Id_tache = %s", (id_tache,))
    tache = cur.fetchone()
    cur.close()
    conn.close()

    # Afficher le formulaire de modification avec les informations de la tâche
    return render_template('modifier_tache.html', tache=tache)

@app.route("/mettre_a_jour/<int:id_tache>", methods=['GET'])
def mettre_a_jour(id_tache):
    # Connexion à la base de données
    conn = mysql.connector.connect(**db_config)
    cur = conn.cursor()

    # Exécution de la requête SQL pour récupérer la tâche à mettre à jour
    cur.execute("SELECT Statue FROM mon_app.Tâche WHERE Id_tache = %s", (id_tache,))
    statue = cur.fetchone()[0]  # Récupérer le statut de la tâche

    # Vérifier le statut actuel et mettre à jour en conséquence
    if statue == 'Non-terminée':
        cur.execute("UPDATE mon_app.Tâche SET Statue = 'Terminée' WHERE Id_tache = %s", (id_tache,))
    else:
        cur.execute("UPDATE mon_app.Tâche SET Statue = 'Non-terminée' WHERE Id_tache = %s", (id_tache,))

    # Validation de la transaction
    conn.commit()

    # Fermeture du curseur et de la connexion
    cur.close()
    conn.close()

    # Redirection vers la page des tâches après la mise à jour
    return redirect("/taches")


@app.route("/rechercher", methods=['GET', 'POST'])
def rechercher_taches():
    if request.method == 'POST':
        terme_recherche = request.form['terme_recherche']

        # Connexion à la base de données
        conn = mysql.connector.connect(**db_config)
        cur = conn.cursor()

        # Exécution de la requête SQL pour rechercher les tâches par titre
        cur.execute("SELECT * FROM mon_app.Tâche WHERE Titre LIKE %s", ("%" + terme_recherche + "%",))
        taches = cur.fetchall()

        # Fermeture du curseur et de la connexion
        cur.close()
        conn.close()

        # Affichage des résultats dans un template
        return render_template('taches.html', taches=taches)

    # Si la méthode est GET, afficher la page de recherche
    return render_template('taches.html')



if __name__ == "__main__":
    app.run(debug=True)

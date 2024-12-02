from flask import Flask, render_template, request, redirect, flash
import os
from werkzeug.utils import secure_filename
import mysql.connector as mysql
import pandas as pd

app = Flask(__name__)

# Définir la clé secrète pour la session
app.config['SECRET_KEY'] = os.urandom(24)

# Configuration du dossier pour stocker les fichiers téléchargés
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'xlsx', 'xls'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Configuration de la base de données
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'indemniter'
}

# Vérifier les extensions de fichier autorisées
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Vérification de la connexion à la base de données
def verify_connection():
    try:
        conn = mysql.connect(**db_config)
        conn.close()
        return True
    except mysql.Error as e:
        print(f"Erreur de connexion à la base de données : {e}")
        return False

# Fonction pour nettoyer les données, remplacer les NaN par une valeur par défaut
def clean_data(data):
    for sheet_name, df in data.items():
        print(f"Feuille lue : {sheet_name}")
        print(df.head())

        if 'SALAIRE' in df.columns:
            df['SALAIRE'] = df['SALAIRE'].fillna(0)
        if 'COMM' in df.columns:
            df['COMM'] = df['COMM'].fillna(0)

        df = df.fillna('')
        data[sheet_name] = df
    return data

# Lire le fichier Excel
def read_excel(file_path):
    try:
        data = pd.read_excel(file_path, sheet_name=None)
        print(f"Lecture réussie du fichier Excel : {file_path}")
        print(f"Feuilles disponibles : {data.keys()}")
        return data
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier Excel : {e}")
        return None

# Insérer les données dans la base de données
def insert_data_to_db(data):
    try:
        conn = mysql.connect(**db_config)
        cursor = conn.cursor()

        # Nettoyer les données avant l'insertion
        data = clean_data(data)

        # Insérer les services
        if "SERVICE" in data:
            for _, row in data["SERVICE"].iterrows():
                print(f"Insertion SERVICE : {row}")  # Affichage avant insertion
                cursor.execute(
                    """INSERT IGNORE INTO SERVICE (NUMSERVICE, NOMSERVICE, LOCALITE)
                    VALUES (%s, %s, %s)""", 
                    (row['NUMSERVICE'], row['NOMSERVICE'], row['LOCALITE'])
                )

        # Insérer les employés
        if "EMPLOYE" in data:
            for _, row in data["EMPLOYE"].iterrows():
                print(f"Insertion EMPLOYE : {row}")  # Affichage avant insertion
                cursor.execute(
                    """INSERT IGNORE INTO EMPLOYE (NUMEMP, NUMSERVICE, EMP_NUMEMP, NOMEMP, FONCTION, DATEEMB, SALAIRE, COMM)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)""", 
                    (row['NUMEMP'], row['NUMSERVICE'], row['EMP_NUMEMP'], row['NOMEMP'],
                     row['FONCTION'], row['DATEEMB'], row['SALAIRE'], row['COMM'])
                )

        # Insérer les indemnités
        if "INDEMNITE" in data:
            for _, row in data["INDEMNITE"].iterrows():
                print(f"Insertion INDEMNITE : {row}")  # Affichage avant insertion
                cursor.execute(
                    """INSERT IGNORE INTO INDEMNITE (CODEIND, NIVEAU, MONTANT)
                    VALUES (%s, %s, %s)""", 
                    (row['CODEIND'], row['NIVEAU'], row['MONTANT'])
                )

        # Insérer les enfants
        if "ENFANT" in data:
            for _, row in data["ENFANT"].iterrows():
                print(f"Insertion ENFANT : {row}")  # Affichage avant insertion
                cursor.execute(
                    """INSERT IGNORE INTO ENFANT (NUMENF, PRENOM, AGE, CODEIND, NUMEMP)
                    VALUES (%s, %s, %s, %s, %s)""", 
                    (row['NUMENF'], row['PRENOM'], row['AGE'], row['CODEIND'], row['NUMEMP'])
                )

        conn.commit()
        print("Insertion des données réussie.")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Erreur lors de l'insertion des données : {e}")

# Route d'upload
@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('Aucun fichier sélectionné')
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash('Aucun fichier sélectionné')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

            file.save(file_path)

            if not verify_connection():
                flash('Connexion à la base de données impossible. Veuillez vérifier la configuration.')
                return redirect(request.url)

            data = read_excel(file_path)
            if data:
                insert_data_to_db(data)
                flash('Données insérées avec succès !')
            else:
                flash('Erreur dans la lecture du fichier Excel.')
            return redirect(request.url)

    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True)

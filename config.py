class Config:
    # Configuration Flask
    SECRET_KEY = ''  # Remplace par une clé secrète sécurisée et aléatoire

    # Configuration de la base de données
    DB_DRIVER = '{MySQL ODBC 8.0 ANSI Driver}'
    DB_SERVER = 'localhost'
    DB_DATABASE = 'indemniter'
    DB_USER = 'root'
    DB_PASSWORD = '_your_password'  # Remplace par ton mot de passe MySQL réel

    # Configuration de l'upload
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'xlsx'}  # Extensions de fichiers autorisées

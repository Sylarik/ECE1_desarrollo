import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firebase
def inicializar_firebase():
    """Conectar con Firebase usando el archivo de credenciales."""
    cred = credentials.Certificate(r"C:\Users\sarag\ECE1_desarrollo\example\ece1desarrollo-firebase-adminsdk-zfg1i-0807573781.json")  # Cambia la ruta
    firebase_admin.initialize_app(cred)
    return firestore.client()

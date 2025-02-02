import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv
import os

load_dotenv()
CREDENTAILS_JSON = os.getenv("CREDENTAILS_JSON")

# Inicializar Firebase
def inicializar_firebase():
    
    if not firebase_admin._apps:
        cred = credentials.Certificate(CREDENTAILS_JSON) 
        firebase_admin.initialize_app(cred)
    return firestore.client()

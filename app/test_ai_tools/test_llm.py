import os
import time
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

# =================================================================
# CONFIGURATION LOCALE (Remplace la Cellule 2 du Colab)
# =================================================================

# 1. Charger les variables d'environnement (.env)
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

if not GOOGLE_API_KEY:
    print("❌ ERREUR : La clé 'GOOGLE_API_KEY' n'est pas trouvée dans le fichier .env")
    exit()
else:
    print("✅ Clé API trouvée.")

# =================================================================
# TEST DU MODÈLE (Adaptation de la Cellule 3 du Colab)
# =================================================================

print("--- Lancement du test de connexion à l'API Google (Local) ---")

try:
    # Tu as accès à gemini-2.5-flash selon ton check_models.py
    test_model_name = "gemini-2.5-flash"
    
    llm_test = ChatGoogleGenerativeAI(
        model=test_model_name,
        google_api_key=GOOGLE_API_KEY,
        temperature=0.1
    )

    print(f"Envoi d'une requête de test au modèle '{test_model_name}'...")
    
    # Mesure du temps de réponse (optionnel mais sympa)
    start_time = time.time()
    response = llm_test.invoke("Bonjour, réponds 'OK' si tu fonctionnes sur mon PC local.")
    end_time = time.time()

    print("\n" + "="*50)
    print(f"✅ SUCCÈS : Le modèle a répondu en {end_time - start_time:.2f} secondes.")
    print(f"🤖 Réponse : '{response.content}'")
    print("="*50)

except Exception as e:
    print("\n" + "="*50)
    print("❌ ERREUR : La vérification a échoué.")
    print(f"Détail : {e}")
    print("="*50)
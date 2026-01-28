# test_google_api.py
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if api_key:
    print("✅ La clé est chargée correctement !")
else:
    print("❌ La clé n'est pas trouvée.")

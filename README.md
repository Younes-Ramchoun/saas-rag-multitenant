SaaS Assistant (RAG multi-tenant)
🧰 Stack utilisée

Python 3.14

FastAPI pour le backend

Streamlit pour l’interface utilisateur

FAISS + SentenceTransformer pour la recherche vectorielle (RAG)

Google Gemini LLM (optionnel, utilisé pour augmenter et reformuler les réponses)

📦 Structure du projet
app/
├── main.py               # API FastAPI
├── rag/
│   └── rag_logic.py      # Logique de recherche vectorielle FAISS
├── tenants/
│   └── __init__.py       # Gestion des tenants et des API keys
├── schemas/
│   └── schemas.py        # Modèles Pydantic
├── services/
│   ├── llm_google_api.py # Intégration LLM
│   └── llm_mock.py       # Version mock (facultative)
├── data/
│   ├── tenantA/          # Documents client A
│   └── tenantB/          # Documents client B
frontend.py               # Interface Streamlit
test_ai_tools/            # Scripts de test LLM / torch
README.md                 # Ce fichier
requirements.txt          # Dépendances
commande.txt              # Commandes pour lancer backend et frontend
.env.example              # Exemple de fichier pour variables d'environnement

🚀 Comment lancer le backend

Activer l’environnement virtuel :

.\.venv\Scripts\Activate.ps1


Lancer FastAPI avec Uvicorn :

uvicorn app.main:app --reload


L’API sera disponible sur : http://127.0.0.1:8000

🖥️ Comment lancer l’interface

Dans un autre terminal, activer l’environnement :

.\.venv\Scripts\Activate.ps1


Se placer dans le dossier app :

cd app


Lancer Streamlit :

streamlit run frontend.py


L’interface s’ouvrira automatiquement dans le navigateur.

🔑 Tester les clients séparément

Sélectionner le tenant via le menu ou bouton Tenant A / Tenant B dans l’interface.

Les requêtes envoyées à l’API sont associées au tenant via le header X-API-KEY.

Les documents de chaque client sont strictement isolés : Tenant A ne voit jamais les documents de Tenant B et vice versa.

Exemples de clés API :

tenantA_key → client A

tenantB_key → client B

🌱 Variables d’environnement

Crée un fichier .env à la racine du projet (ou .env.local) avec :

GOOGLE_API_KEY=ta_cle_api_google


Cette clé est utilisée pour l’augmentation des réponses avec le LLM Google Gemini.

Si tu n’as pas de clé, le système fonctionne quand même avec la recherche vectorielle FAISS.

💡 Approche technique

Séparation multi-tenant

Gestion côté serveur via le header X-API-KEY et le dictionnaire TENANTS.

Chaque tenant a son propre dossier de documents et son index FAISS.

Recherche vectorielle (RAG)

FAISS + SentenceTransformer pour encoder les documents et trouver les plus pertinents par question.

Les doublons sont filtrés et les documents hors-sujet sont ignorés pour éviter des réponses incorrectes.

Gestion des cas sans réponse

Si aucune information pertinente n’est trouvée pour une question, l’API renvoie :
"Aucune information disponible pour votre question."

Augmentation avec LLM (optionnel / bonus)

Google Gemini utilisé pour reformuler et synthétiser les documents récupérés.

Intégré après validation que le RAG retourne correctement les informations essentielles.

Interface utilisateur

Streamlit permet au client de sélectionner son tenant, poser des questions et afficher les réponses de manière claire.

⚡ Commandes utiles (commande.txt)

Terminal 1 : backend FastAPI

.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload


Terminal 2 : interface Streamlit

.\.venv\Scripts\Activate.ps1
cd app
streamlit run frontend.py

📝 Exemple de test

Question Tenant A : “Comment résilier un contrat ?”
Réponse attendue :

Procédure résiliation
La résiliation doit être enregistrée dans le CRM.
Un accusé de réception est envoyé sous 48h.
Le responsable conformité valide les dossiers sensibles.


Question Tenant B : “Comment résilier un contrat ?”
Réponse attendue :

Aucune information disponible pour votre question.


✅ Ce README couvre tout ce qu’un recruteur a besoin pour tester ton projet facilement, voir la séparation des tenants, et comprendre ton approche technique.
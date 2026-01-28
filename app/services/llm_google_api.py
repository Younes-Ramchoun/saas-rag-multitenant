# app/services/llm_google_api.py
from langchain_google_genai import ChatGoogleGenerativeAI
from dotenv import load_dotenv
import os

# Charger le .env pour être sûr que GOOGLE_API_KEY est présent
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("❌ GOOGLE_API_KEY non trouvée dans le .env")

def augment_response_with_llm(documents: list, question: str) -> str:
    """
    Envoie les documents et la question au LLM pour générer une réponse augmentée.
    """
    if not documents:
        return "Aucune information disponible pour votre question."

    # Préparer le prompt
    context = "\n\n".join(documents)
    prompt = (
         f"Tu es un assistant virtuel professionnel. Voici les informations disponibles :\n\n"
    f"{context}\n\n"
    f"Question du client : {question}\n\n"
    f"Réponds de manière naturelle et professionnelle, comme si tu parlais directement au client. "
    f"Sois clair, concis et utilise uniquement les informations fournies ci-dessus."
    f"Si les informations ne sont pas suffisantes, réponds honnêtement que tu n'as pas assez de données."
    )

    # ⚡ IMPORTANT : utiliser 'api_key' et non 'google_api_key'
    llm = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash",
        api_key=GOOGLE_API_KEY,
        temperature=0.1
    )

    response = llm.invoke(prompt)
    return response.content

import streamlit as st
import requests

st.title("ActuData RAG Multi-Tenant")

# Choix du tenant via radio button
tenant_choice = st.radio("Choisir le client :", ("Tenant A", "Tenant B"))

# Associer le tenant choisi à l'API Key correspondante
tenant_api_keys = {
    "Tenant A": "tenantA_key",
    "Tenant B": "tenantB_key"
}
api_key = tenant_api_keys[tenant_choice]

# Question
question = st.text_input("Votre question")

# Bouton pour envoyer la requête
if st.button("Envoyer"):
    if not question:
        st.warning("Veuillez entrer une question.")
    else:
        # Appel API POST
        response = requests.post(
            "http://127.0.0.1:8000/query",
            headers={"X-API-KEY": api_key},
            json={"question": question}
        )
        if response.status_code == 200:
            data = response.json()
            st.subheader("Réponse")
            st.write(data["answer"])
        else:
            st.error(f"Erreur {response.status_code}: {response.text}")

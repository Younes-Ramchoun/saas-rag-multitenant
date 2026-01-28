# app/rag/rag_logic.py
import os
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

class RAG:
    def __init__(self, tenant_name: str, data_path="app/data"):
        self.tenant_name = tenant_name
        self.data_path = os.path.join(data_path, tenant_name)
        self.index_file = os.path.join(self.data_path, "index.faiss")
        self.texts_file = os.path.join(self.data_path, "texts.npy")
        self.model = SentenceTransformer("all-MiniLM-L6-v2")
        self.texts = []

        # Charger ou créer l'index
        if os.path.exists(self.index_file) and os.path.exists(self.texts_file):
            self._load_index()
        else:
            self._build_index()

    def _load_index(self):
        print(f"📂 Chargement de l'index FAISS pour {self.tenant_name}...")
        self.index = faiss.read_index(self.index_file)
        self.texts = np.load(self.texts_file, allow_pickle=True).tolist()
        print(f"✅ Index chargé avec {len(self.texts)} documents.")

    def _build_index(self):
        print(f"⚡ Création d'un nouvel index FAISS pour {self.tenant_name}...")
        self.texts = self._load_documents()
        if not self.texts:
            self.index = None
            print(f"⚠️ Aucun document trouvé pour {self.tenant_name}")
            return

        embeddings = self.model.encode(self.texts, convert_to_numpy=True)
        dim = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dim)
        self.index.add(embeddings)

        os.makedirs(self.data_path, exist_ok=True)
        faiss.write_index(self.index, self.index_file)
        np.save(self.texts_file, np.array(self.texts, dtype=object))
        print(f"✅ Index créé et sauvegardé avec {len(self.texts)} documents.")

    def _load_documents(self):
        """Charge les documents TXT du tenant, en supprimant les doublons."""
        docs = []
        seen_texts = set()
        for fname in os.listdir(self.data_path):
            if fname.endswith(".txt"):
                path = os.path.join(self.data_path, fname)
                with open(path, "r", encoding="utf-8") as f:
                    text = f.read().strip()
                    if text and text not in seen_texts:
                        docs.append(text)
                        seen_texts.add(text)
                        print(f"Chargement de {fname} pour {self.tenant_name}")
                    elif text in seen_texts:
                        print(f"Doublon ignoré : {fname} pour {self.tenant_name}")
        return docs

    def search(self, query: str, k: int = 3):
        """Recherche vectorielle avec FAISS et filtrage minimal par mot-clé."""
        if not self.texts or not self.index:
            return []

        q_vec = self.model.encode([query], convert_to_numpy=True)
        D, I = self.index.search(q_vec, k)

        # Récupérer les résultats uniques
        results = [self.texts[i] for i in I[0] if i < len(self.texts)]

        # Filtrage minimal : renvoyer seulement les documents contenant au moins un mot de la question
        query_words = set(query.lower().split())
        filtered = []
        for r in results:
            r_words = set(r.lower().split())
            if query_words & r_words:  # intersection non vide
                filtered.append(r)

        return filtered

# app/main.py
from fastapi import FastAPI, Header, HTTPException, Depends
from .rag.rag_logic import RAG
from .schemas.schemas import QueryRequest, QueryResponse
from .tenants import get_tenant_from_key
from .services.llm_google_api import augment_response_with_llm

app = FastAPI()

# Cache des RAG par tenant
rag_instances = {}

def get_rag(api_key: str = Header(..., alias="X-API-KEY")):
    try:
        tenant = get_tenant_from_key(api_key)
    except ValueError:
        raise HTTPException(status_code=401, detail="API Key invalide")
    
    if tenant not in rag_instances:
        rag_instances[tenant] = RAG(tenant_name=tenant)
    return rag_instances[tenant], tenant

@app.post("/query", response_model=QueryResponse)
def query(request: QueryRequest, rag_tenant=Depends(get_rag)):
    rag, tenant = rag_tenant
    results = rag.search(request.question, k=3)
    
    # Si aucun document pertinent trouvé
    if not results:
        answer = "Aucune information disponible pour votre question."
    else:
        #answer = "\n---\n".join(results)
        answer = augment_response_with_llm(results, request.question)

    return QueryResponse(tenant=tenant, answer=answer)

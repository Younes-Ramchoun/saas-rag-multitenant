# app/tenants/__init__.py

TENANTS = {
    "tenantA_key": "tenantA",
    "tenantB_key": "tenantB",
}

def get_tenant_from_key(api_key: str):
    tenant = TENANTS.get(api_key)
    if not tenant:
        raise ValueError("API Key invalide")
    return tenant

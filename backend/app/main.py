from fastapi import FastAPI
from app.api import endpoints_ponto, endpoints_user, endpoints_auth

app = FastAPI(title="Conecta Trabalhador - Backend")

# Routers
app.include_router(endpoints_auth.router)
app.include_router(endpoints_user.router)
app.include_router(endpoints_ponto.router)

@app.get("/")
def health_check():
    return {"status": "ok"}

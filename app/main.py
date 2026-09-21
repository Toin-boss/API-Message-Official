"""Ponto de entrada do FastAPI e definição das rotas.

Estrutura inicial; implementação pendente.
"""
from fastapi import FastAPI
from app.webhook import router


app = FastAPI()
app.include_router(router)

@app.get("/status")
async def root():
    return {"status":"OK"}
"""Ponto de entrada do FastAPI e definição das rotas.

Estrutura inicial; implementação pendente.
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/status")
async def root():
    return {"status":"OK"}
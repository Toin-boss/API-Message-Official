"""Recepção de eventos e validação do webhook da Meta.

Estrutura inicial; implementação pendente.
"""
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Query, HTTPException
from typing import Annotated
from fastapi.responses import PlainTextResponse


load_dotenv()
VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")

router = APIRouter()

@router.get("/webhook", response_class=PlainTextResponse)
async def verify_webhook(hub_mode: Annotated[str, Query(alias="hub.mode")],      #Indicates the operation
                         hub_verify_token: Annotated[str, Query(alias="hub.verify_token")],       #Token to be compared
                         hub_challenge: Annotated[str, Query(alias="hub.challenge")]):      #Challenge that we will return after validating the request.
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:    
        return PlainTextResponse(hub_challenge)

    raise HTTPException(status_code=403, detail="Verificação inválida")
    
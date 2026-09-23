"""Recepção de eventos e validação do webhook da Meta.

Estrutura inicial; implementação pendente.
"""
import os, hmac, hashlib, logging
from json import JSONDecodeError
from dotenv import load_dotenv
from fastapi import APIRouter, Query, HTTPException, Request
from typing import Annotated
from fastapi.responses import PlainTextResponse


load_dotenv()

VERIFY_TOKEN = os.getenv("META_VERIFY_TOKEN")
APP_SECRET = os.getenv("META_APP_SECRET")

if not APP_SECRET:
    raise RuntimeError("META_APP_SECRET não configurado")
if not VERIFY_TOKEN:
    raise RuntimeError("META_VERIFY_TOKEN não configurado")

router = APIRouter()
logger = logging.getLogger("uvicorn.error")

#Validating webhook authentication
@router.get("/webhook", response_class=PlainTextResponse)
async def verify_webhook(hub_mode: Annotated[str, Query(alias="hub.mode")],      #Indicates the operation
                         hub_verify_token: Annotated[str, Query(alias="hub.verify_token")],       #Token to be compared
                         hub_challenge: Annotated[str, Query(alias="hub.challenge")]):      #Challenge that we will return after validating the request.
    if hub_mode == "subscribe" and hub_verify_token == VERIFY_TOKEN:    
        return PlainTextResponse(hub_challenge)

    raise HTTPException(status_code=403, detail="Verificação inválida")


@router.post("/webhook")
async def receive_webhook(request: Request):

    #Calculation of the expected signature
    body = await request.body()
    signature = request.headers.get("X-Hub-Signature-256")
    expected_signature = "sha256=" + hmac.new(APP_SECRET.encode("utf-8") ,body, hashlib.sha256).hexdigest()
    
    if not signature or not hmac.compare_digest(signature, expected_signature):
        raise HTTPException(status_code=403, detail="Assinatura inválida")

    #Interpretation of the request body as JSON
    try: 
        payload = await request.json() #Checking if the body is in JSON format

    except JSONDecodeError:
        raise HTTPException(status_code=400, detail="JSON inválido") 

    if not isinstance(payload, dict):
        raise HTTPException(status_code=400, detail="O corpo deve ser o objeto JSON")

    #Checking if the event belongs to the Whatsapp Business account
    if payload.get("object") != "whatsapp_business_account":
        raise HTTPException(status_code=400, detail="Objeto do webhook não suportado")

    entries = payload.get("entry")
    if not isinstance(entries, list):
        raise HTTPException(status_code=400, detail="O campo entry deve ser uma lista")

    for entry in entries:    #Checking if each element of the list entry is a dict
        if not isinstance(entry, dict): 
            raise HTTPException(status_code=400, detail="Cada item de entry deve ser um objeto JSON")

        #Checking if the element changes is a list
        changes = entry.get("changes")
        if not isinstance(changes, list):
            raise HTTPException(status_code=400, detail="O campo changes deve ser uma lista")
      
        for change in changes:   #Checking if each element of the list change is a dict
            if not isinstance(change, dict):
                raise HTTPException(status_code=400, detail="Cada item de changes deve ser um objeto JSON")

            if change.get("field") != "messages": 
                continue

            #Checking if the element value is a dict    
            value = change.get("value")
            if not isinstance(value, dict):  
                raise HTTPException(status_code=400, detail="O campo value deve ser um objeto JSON")

            messages = value.get("messages", [])
            if not isinstance(messages, list):
                raise HTTPException(status_code=400, detail="O campo messsages deve ser um lista")

            for message in messages:   #Cheking if each elemente of the list messages is a dict
                if not isinstance(message, dict):
                    raise HTTPException(status_code=400, detail="Cada item de mensagens dever ser um objeto JSON")

                message_id = message.get("id")
                sender = message.get("from")
                message_type = message.get("type")

                if message_type != "text":
                    continue

                text_data = message.get("text")

                #Checking if the element text is a dict
                if not isinstance(text_data, dict):
                    raise HTTPException(status_code=400, detail="O campo text deve ser um objeto JSON")

                message_text = text_data.get("body")

                if not isinstance(message_text, str):
                    raise HTTPException(status_code=400, detail="O campo text.body deve ser uma string")

                logger.info("Mensagem de texto recebida")
                
    return PlainTextResponse("EVENT_RECEIVED", status_code=200)
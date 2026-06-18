import os
import logging
import requests
from supabase import create_client, Client
from dotenv import load_dotenv

# --- CONFIG -------------------------------------------------------------------

load_dotenv()
 
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger(__name__)

SUPABASE_URL: str = os.environ["SUPABASE_URL"]
SUPABASE_KEY: str = os.environ["SUPABASE_KEY"]

ZAPI_INSTANCE_ID: str = os.environ["ZAPI_INSTANCE_ID"]
ZAPI_TOKEN: str = os.environ["ZAPI_TOKEN"]
ZAPI_CLIENT_TOKEN: str = os.environ["ZAPI_CLIENT_TOKEN"]

MAX_CONTACTS = 3

# --- SUPABASE -----------------------------------------------------------------

def fetch_contacts(client: Client) -> list[dict]:
    logger.info("Buscando contatos no Supabase...")
    
    response = (
        client.table("contatos")
        .select("nome, contato")
        .limit(MAX_CONTACTS)
        .execute()
    )
    contacts = response.data

    logger.info(f"{len(contacts)} contato(s) encontrado(s).")
    return contacts

# --- Z-API --------------------------------------------------------------------

def send_wpp_message(phone: str, message: str) -> bool:
    url = (
        f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}"
        f"/token/{ZAPI_TOKEN}/send-text"
    )

    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN,
    }
    payload = {
        "phone": phone,
        "message": message,
    }

    try:
        response = requests.post(url, json=payload, headers=headers, timeout=15)
        response.raise_for_status()
        logger.info(f"Mensagem enviada para {phone}.")
        return True
    
    except requests.exceptions.HTTPError as e:
        logger.error(f"Erro HTTP ao enviar para {phone}: {e} — {response.text}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Erro de conexão ao enviar para {phone}: {e}")
    return False

# --- MAIN ---------------------------------------------------------------------

def main() -> None:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    contacts = fetch_contacts(supabase)

    if not contacts:
        logger.warning("Erro: Nenhum contato encontrado, Encerrando...")
        return
    
    success_count = 0
    for contact in contacts:
        name: str = contact.get("nome", "").strip()
        phone: str = contact.get("contato", "").strip()

        if not name or not phone:
            logger.warning(f"Contato inválido (sem nome ou telefone): {contact}")
            continue

        message = f"Olá, {name} tudo bem com você?"
        logger.info(f"Enviando mensagem para {name} ({phone})...")

        if(send_wpp_message(phone, message)):
            success_count += 1
    
    logger.info(f"Concluído - {success_count}/{len(contacts)} mensagem(ns) enviada(s) com sucesso.")

if __name__ == "__main__":
    main()
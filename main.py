import os
import logging
import requests
from supabase import create_client, Client
from dotenv import load_dotenv

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

def send_wpp_message():
    pass

def main() -> None:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    contacts = fetch_contacts(supabase)

if __name__ == "__main__":
    main()
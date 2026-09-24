#Connection of the database in API
import os, psycopg
from dotenv import load_dotenv
from psycopg.types.json import Jsonb

load_dotenv()

host = os.getenv("POSTGRES_HOST")
port = os.getenv("POSTGRES_PORT")
dbname = os.getenv("POSTGRES_DB")
user = os.getenv("POSTGRES_USER")
password = os.getenv("POSTGRES_PASSWORD")

#Conection in database
def get_connection():
    return psycopg.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )

#Save the message into database
def save_message(message_id, sender, sent_at, message_type, text_body, payload):

    sql = """INSERT INTO messages (message_id, sender, sent_at, message_type, text_body, payload)
                VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (message_id) DO NOTHING"""

    with get_connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(sql,(message_id, sender, sent_at, message_type, text_body, Jsonb(payload)))




import psycopg2
import os
from dotenv import load_dotenv


# Load .env variables
load_dotenv()

## Helper funcs ##

def get_postgres_url_aws():
    db_host = 'fandomdbinstance.cil0ke6w208h.us-east-1.rds.amazonaws.com'
    db_name = 'fandomdb'
    db_user = 'fandomdbadmin'
    db_pass = 'myteamdb5'

    return f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"
    
def get_postgres_url_render():
    url = 'postgresql://fandomdotcom_db_user:cSKQ7VSxozh6V8GQItWP1X1nWQb7Erqi@dpg-d6eh20buibrs73dbuau0-a.ohio-postgres.render.com/fandomdotcom_db'
    return url
    
def get_postgres_url_local():
    return os.getenv('DATABASE_URL')
    

## Connection funcs ##

def connect_render():
    url = get_postgres_url_render()
    print(url)
    connection = psycopg2.connect(url)
    print('Connected to render postgres database')
    return connection

def connect_aws():
    url = get_postgres_url_aws()
    print(url)
    connection = psycopg2.connect(url)
    print('Connected to aws postgres database')
    return connection

def connect_local():
    url = get_postgres_url_local()
    print(url)
    connection = psycopg2.connect(url)
    print('Connected to local postgres database')
    return connection

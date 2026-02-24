
import psycopg2
import os
from dotenv import load_dotenv


# Load .env variables
load_dotenv()

# DB Constants
db_host = 'fandomdbinstance.cil0ke6w208h.us-east-1.rds.amazonaws.com'
db_name = 'fandomdb'
db_user = 'fandomdbadmin'
db_pass = 'myteamdb5'


## Helper funcs ##

def get_postgres_url_aws():
    return f"postgresql://{db_user}:{db_pass}@{db_host}:5432/{db_name}"
    
def get_postgres_url_local():
    return os.getenv('DATABASE_URL')
    

## Connection funcs ##

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

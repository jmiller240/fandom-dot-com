
import sqlalchemy
import psycopg2
import sys

import pandas as pd

from connect_postgres import get_postgres_url_local, get_postgres_url_aws, get_postgres_url_render


def create_database(loc: str):

    # Get url
    url = ''
    if loc == 'local':
        url = get_postgres_url_local()
    elif loc == 'aws':
        url = get_postgres_url_aws()
    elif loc == 'render':
        url = get_postgres_url_render()
    else:
        raise ValueError('Parameter "loc" must be "local" or "aws" or "render".')
    
    # Connect
    connection = psycopg2.connect(url)
    print('Connected to database')

    # Get table definition queries
    db_creation_sql = open('create_db.sql', 'r+').read()
    queries = [q.strip() for q in db_creation_sql.split(';')]

    # Create tables
    cursor = connection.cursor()

    for q in queries:
        if not q: continue
        
        print(q)
        cursor.execute(q)
        print('Query complete.')

    print('All done.')
    cursor.close()
    connection.commit()


def populate_database(loc: str):

    # Get url
    url = ''
    if loc == 'local':
        url = get_postgres_url_local()
    elif loc == 'aws':
        url = get_postgres_url_aws()
    elif loc == 'render':
        url = get_postgres_url_render()
    else:
        raise ValueError('Parameter "loc" must be "local" or "aws" or "render"')
    
    # Connect
    engine = sqlalchemy.create_engine(url)
    print('Connected to database')

    # Insert
    for table in ['account', 'league', 'team', 'account_team']:
        
        # read file
        print(f'Reading {table}...')
        df = pd.read_csv(f'data/{table}.csv')
        print(df.head())

        # insert
        print(f'Inserting...')
        rows_inserted = df.to_sql(table, engine, schema='fandom_site', index=False, if_exists='append')
        print(f'Data inserted. {rows_inserted} rows')

if __name__ == '__main__':
    loc = ''
    if len(sys.argv) > 1:
        loc = sys.argv[1]
        create_database(loc=loc)
        populate_database(loc=loc)

    else:
        print(f'No arguments provided.')

    